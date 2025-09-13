import axios from "axios";
import React, { useState, useEffect } from 'react';
import './UserList.css'; 

function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get("https://manage-user-list.onrender.com/users")
      .then(response => {
        setUsers(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching users:", error);
        setError("خطا در بارگذاری کاربران. مطمئن شوید سرور در حال اجراست.");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="alert alert-info text-center" role="alert">
          در حال بارگذاری کاربران...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger text-center" role="alert">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-5" dir="rtl">
      <h2 className="mb-4 text-center">لیست کاربران</h2>
      {users.length === 0 ? (
        <div className="alert alert-warning text-center" role="alert">
          هیچ کاربری پیدا نشد.
        </div>
      ) : (
        <div className="table-responsive">
          <table className="table table-bordered align-middle text-center user-table">
            <thead className="table-dark">
              <tr>
                <th scope="col">شناسه</th>
                <th scope="col">نام</th>
                <th scope="col">ایمیل</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user, index) => (
                <tr key={user.id} className={index % 2 === 0 ? "even-row" : "odd-row"}>
                  <td>{index + 1}</td>
                  <td>{user.username}</td>
                  <td>
                    <a
                      href={`mailto:${user.email}`}
                      className="email-link"
                    >
                      {user.email}
                    </a>
                  </td>
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
