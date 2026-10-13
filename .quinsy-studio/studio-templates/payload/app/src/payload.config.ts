import { postgresAdapter } from '@payloadcms/db-postgres'
import { resendAdapter } from '@payloadcms/email-resend'
import { lexicalEditor } from '@payloadcms/richtext-lexical'
import { s3Storage } from '@payloadcms/storage-s3'
import path from 'path'
import { buildConfig } from 'payload'
import { fileURLToPath } from 'url'

import { Media } from './collections/Media'
import { Users } from './collections/Users'

const filename = fileURLToPath(import.meta.url)
const dirname = path.dirname(filename)

// `next build` runs without runtime secrets; every other phase must fail fast.
const building = process.env.NEXT_PHASE === 'phase-production-build'

function requireEnv(name: string): string {
  const value = process.env[name]
  if (value) return value
  if (building) return ''
  throw new Error(`${name} is not set. Add it with ./studio env <project> ... --approve.`)
}

const s3Configured = Boolean(process.env.S3_ACCESS_KEY_ID && process.env.S3_SECRET_ACCESS_KEY)

export default buildConfig({
  admin: {
    user: Users.slug,
    importMap: {
      baseDir: path.resolve(dirname),
    },
  },
  collections: [Users, Media],
  editor: lexicalEditor(),
  secret: requireEnv('PAYLOAD_SECRET'),
  typescript: {
    outputFile: path.resolve(dirname, 'payload-types.ts'),
  },
  db: postgresAdapter({
    pool: {
      connectionString: requireEnv('DATABASE_URL'),
    },
    push: process.env.NODE_ENV !== 'production',
  }),
  email: process.env.RESEND_API_KEY
    ? resendAdapter({
        defaultFromAddress: process.env.RESEND_FROM || 'studio@localhost',
        defaultFromName: '{{PROJECT}}',
        apiKey: process.env.RESEND_API_KEY,
      })
    : undefined,
  localization: {
    locales: ['en'],
    defaultLocale: 'en',
    fallback: true,
  },
  plugins: s3Configured
    ? [
        s3Storage({
          collections: {
            media: true,
          },
          bucket: process.env.S3_BUCKET || 'media',
          config: {
            credentials: {
              accessKeyId: requireEnv('S3_ACCESS_KEY_ID'),
              secretAccessKey: requireEnv('S3_SECRET_ACCESS_KEY'),
            },
            region: process.env.S3_REGION || 'auto',
            endpoint: process.env.S3_ENDPOINT || undefined,
            forcePathStyle: true,
          },
        }),
      ]
    : [],
})
