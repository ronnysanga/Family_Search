import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

// Define una API base que podemos inyectar en los puntos finales según sea necesario
export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ 
    baseUrl: 'http://localhost:3001/api', // Ajusta esta URL según tu backend
    prepareHeaders: (headers) => {
      // Aquí puedes agregar headers comunes como tokens de autenticación
      // const token = getAuthToken();
      // if (token) {
      //   headers.set('authorization', `Bearer ${token}`);
      // }
      return headers;
    },
  }),
  tagTypes: ['User', 'Users'], // Define tags para invalidación de caché
  endpoints: () => ({}), // Los endpoints se inyectan en archivos separados
});
