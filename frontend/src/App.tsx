import './App.css';
import UserList from './features/users/UserList';

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Family Search</h1>
      </header>
      <main>
        <UserList />
      </main>
    </div>
  );
}

export default App;
