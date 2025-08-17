import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

// Define una API base que podemos inyectar en los puntos finales según sea necesario
// Mostrar la URL de la API que se está utilizando
console.log('API URL:', import.meta.env.VITE_API_URL || 'http://localhost:3001/api (default)');

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ 
    baseUrl: import.meta.env.VITE_API_URL || 'http://localhost:3001/api',
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
