import { describe, expect, it, vi } from "vitest";
import {
  isClientExposedEnvName,
  pickServerOnlySecret,
  revalidateAfterWrite,
} from "./write-side-revalidate";

describe("pickServerOnlySecret", () => {
  it("skips NEXT_PUBLIC_ keys even when they have a value", () => {
    const env = {
      NEXT_PUBLIC_REVALIDATE_SECRET: "public-leak",
      REVALIDATE_SECRET: "server-only",
    };
    expect(
      pickServerOnlySecret(env, [
        "NEXT_PUBLIC_REVALIDATE_SECRET",
        "REVALIDATE_SECRET",
      ]),
    ).toBe("server-only");
  });

  it("returns empty when only client-exposed keys are listed", () => {
    const env = { NEXT_PUBLIC_INTERNAL_URL: "https://delivery.example" };
    expect(pickServerOnlySecret(env, ["NEXT_PUBLIC_INTERNAL_URL"])).toBe("");
  });
});

describe("isClientExposedEnvName", () => {
  it("flags NEXT_PUBLIC_ names", () => {
    expect(isClientExposedEnvName("NEXT_PUBLIC_DELIVERY_URL")).toBe(true);
    expect(isClientExposedEnvName("INTERNAL_DELIVERY_URL")).toBe(false);
  });
});

describe("revalidateAfterWrite", () => {
  it("skips when origin or secret is missing", async () => {
    const fetchImpl = vi.fn();
    expect(
      await revalidateAfterWrite({ origin: "", secret: "s", fetchImpl }),
    ).toBe("skipped");
    expect(
      await revalidateAfterWrite({
        origin: "http://delivery.test",
        secret: "",
        fetchImpl,
      }),
    ).toBe("skipped");
    expect(fetchImpl).not.toHaveBeenCalled();
  });

  it("posts the secret header to the delivery revalidate path", async () => {
    const fetchImpl = vi.fn(async () => new Response(null, { status: 200 }));
    const result = await revalidateAfterWrite({
      origin: "http://delivery.test/",
      secret: "server-only",
      payload: { host: "example.com" },
      fetchImpl,
    });
    expect(result).toBe("ok");
    expect(fetchImpl).toHaveBeenCalledTimes(1);
    expect(fetchImpl).toHaveBeenCalledWith(
      "http://delivery.test/api/revalidate",
      expect.objectContaining({
        method: "POST",
        headers: expect.objectContaining({
          "x-revalidate-secret": "server-only",
        }),
        body: JSON.stringify({ host: "example.com" }),
      }),
    );
  });

  it("returns failed without throwing when the ping errors", async () => {
    const fetchImpl = vi.fn(async () => {
      throw new Error("network");
    });
    await expect(
      revalidateAfterWrite({
        origin: "http://delivery.test",
        secret: "s",
        fetchImpl,
      }),
    ).resolves.toBe("failed");
  });
});
