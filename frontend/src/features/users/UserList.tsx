import React from 'react';
import { useGetUsersQuery } from './usersApi';

const UserList: React.FC = () => {
  // Usa el hook generado automáticamente
  const { data: users, isLoading, isError, isSuccess } = useGetUsersQuery();

  // Mostrar estado de carga
  if (isLoading) {
    return <div>Cargando usuarios...</div>;
  }

  // Mostrar error si lo hay
  if (isError) {
    return <div>Error al cargar los usuarios</div>;
  }

  // Mostrar la lista de usuarios
  return (
    <div>
      <h2>Lista de Usuarios</h2>
      {isSuccess && users && users.length > 0 ? (
        <ul>
          {users.map((user) => (
            <li key={user.id_usuario}>
              {user.nombres} {user.apellidos} - {user.email}
            </li>
          ))}
        </ul>
      ) : (
        <p>No hay usuarios para mostrar</p>
      )}
    </div>
  );
};

export default UserList;
