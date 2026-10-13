import type { Access, CollectionConfig, FieldAccess } from 'payload'

const isAdmin = (user: unknown): boolean =>
  Boolean(user && (user as { role?: string }).role === 'admin')

const adminOrSelf: Access = ({ req: { user } }) => {
  if (!user) return false
  if (isAdmin(user)) return true
  return { id: { equals: user.id } }
}

const adminOnly: Access = ({ req: { user } }) => isAdmin(user)

const adminOnlyField: FieldAccess = ({ req: { user } }) => isAdmin(user)

export const Users: CollectionConfig = {
  slug: 'users',
  auth: {
    maxLoginAttempts: 5,
    lockTime: 10 * 60 * 1000,
  },
  admin: { useAsTitle: 'email' },
  hooks: {
    beforeChange: [
      async ({ data, operation, req }) => {
        if (operation !== 'create') return data
        const { totalDocs } = await req.payload.count({ collection: 'users', req })
        return { ...data, role: totalDocs === 0 ? 'admin' : (data.role ?? 'user') }
      },
    ],
  },
  access: {
    admin: ({ req: { user } }) => isAdmin(user),
    create: () => true,
    read: adminOrSelf,
    update: adminOrSelf,
    delete: adminOnly,
  },
  fields: [
    {
      name: 'role',
      type: 'select',
      required: true,
      defaultValue: 'user',
      options: ['user', 'admin'],
      saveToJWT: true,
      access: {
        create: adminOnlyField,
        update: adminOnlyField,
      },
    },
  ],
}
