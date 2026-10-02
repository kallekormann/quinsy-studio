# split-flap

**Atomic level:** Molecule (`ui-molecule`)

A row of character flaps. When a character changes, that flap rotates in place around a hinge. It does not slide in from below.

`cascade` cycles each flap through the charset, then settles on the target from left to right.

Styled only with semantic tokens. The caller supplies the text and the size (`font-size` on the board sets the flap size).

Pull: `./studio library pull <project> split-flap`
