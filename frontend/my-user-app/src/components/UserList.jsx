    // src/components/UserList.jsx
    import axios from "axios";
    import React, { useState, useEffect } from 'react';

    function UserList() {
      const [users, setUsers] = useState([]);
      const [loading, setLoading] = useState(true);
      const [error, setError] = useState(null);

      useEffect(() => {
        
        axios.get("http://localhost:8000/users")
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
          })
          .then(data => {
            setUsers(data);
            setLoading(false);
          })
          .catch(error => {
            console.error("Error fetching users:", error);
            setError("خطا در بارگذاری کاربران. مطمئن شوید سرور  در حال اجراست.");
            setLoading(false);
          });
      }, []);

      if (loading) {
        return (
          <div className="container mt-5">
            <div className="alert alert-info" role="alert">

              در حال بارگذاری کاربران...
            </div>

          </div>
        );
      }

      if (error) {
        return (
          <div className="container mt-5">
            <div className="alert alert-danger" role="alert">
              {error}
            </div>

          </div>
        );
      }

      return (
        <div className="container mt-5">
          <h2 className="mb-4 text-center">لیست کاربران</h2>
          {users.length === 0 ? (
            <div className="alert alert-warning text-center" role="alert">
              هیچ کاربری پیدا نشد.
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table table-striped table-hover">
                <thead className="table-dark">

                  <tr>
                    
                    <th scope="col">#</th>
                    <th scope="col">نام</th>
                    <th scope="col">ایمیل</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user, index) => (
                    <tr key={user.id}>
                      <th scope="row">{index + 1}</th>
                      <td>{user.username}</td>
                      <td>{user.email}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      );
    }

    export default UserList;
