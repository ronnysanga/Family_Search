import { apiSlice } from '../api/apiSlice';

// Tipos para TypeScript basados en la estructura de la tabla 'usuario'
export interface User {
  id_usuario: number;
  nombres: string;
  apellidos: string;
  email: string;
  password?: string; // Opcional ya que solo se usa para crear/actualizar
  fecha_creacion_usuario?: string; // Timestamp como string
}

// Extendemos el API slice con endpoints específicos para usuarios
export const usersApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    // Obtener todos los usuarios
    getUsers: builder.query<User[], void>({
      query: () => '/users',
      // Proporciona etiquetas para el cacheo y actualización
      providesTags: (result = []) => [
        'Users',
        ...result.map(({ id_usuario }) => ({ type: 'User' as const, id: id_usuario })),
      ],
    }),
    
    // Obtener un usuario por ID
    getUserById: builder.query<User, number>({
      query: (id_usuario) => `/users/${id_usuario}`,
      providesTags: (result, error, id_usuario) => [{ type: 'User' as const, id: id_usuario }],
    }),
    
    // Crear un nuevo usuario
    createUser: builder.mutation<User, Partial<User>>({
      query: (user) => ({
        url: '/users',
        method: 'POST',
        body: user,
      }),
      // Invalida la lista de usuarios para forzar una nueva carga
      invalidatesTags: ['Users'],
    }),
    
    // Actualizar un usuario existente
    updateUser: builder.mutation<User, Partial<User> & Pick<User, 'id_usuario'>>({
      query: ({ id_usuario, ...patch }) => ({
        url: `/users/${id_usuario}`,
        method: 'PATCH',
        body: patch,
      }),
      // Invalida tanto el usuario específico como la lista de usuarios
      invalidatesTags: (result, error, { id_usuario }) => [
        { type: 'User' as const, id: id_usuario },
        'Users',
      ],
    }),
    
    // Eliminar un usuario
    deleteUser: builder.mutation<{ success: boolean; id_usuario: number }, number>({
      query: (id) => ({
        url: `/users/${id}`,
        method: 'DELETE',
      }),
      // Invalida la lista de usuarios
      invalidatesTags: ['Users'],
    }),
  }),
});

// Exporta los hooks generados automáticamente
export const {
  useGetUsersQuery,
  useGetUserByIdQuery,
  useCreateUserMutation,
  useUpdateUserMutation,
  useDeleteUserMutation,
} = usersApiSlice;
