    // src/App.jsx
    import React from 'react';
    import './App.css'; 
    import UserList from './components/UserList';

    function App() {
      return (
        <div className="App">
          <nav className="navbar navbar-dark bg-dark">
            <div className="container-fluid">
            
              <span className="navbar-brand mb-0 h1 ms-auto">اپلیکیشن مدیریت کاربران</span>
              
            </div>
          </nav>
          <UserList />
        </div>
      );
    }

    export default App;
