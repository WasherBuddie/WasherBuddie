import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Header from "./Header";

function UserPreferences() {
  const [email, setEmail] = useState("");
  const [reEmail, setReEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rePassword, setRePassword] = useState("");
  const [phone, setPhone] = useState("");
  const [rePhone, setRePhone] = useState("");
  const [notification, setNotification] = useState("email");
  const [isAdmin, setIsAdmin] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAdminStatus = async () => {
      try {
        const response = await fetch("/get_admin");
        const data = await response.json();
        if (response.ok) {
          setIsAdmin(data.admin);
        } else {
          console.error("Failed to fetch admin status:", data.error);
        }
      } catch (err) {
        console.error("Error fetching admin status:", err);
      }
    };

    fetchAdminStatus();
  }, []);

  const handleEmailUpdate = async (e) => {
    e.preventDefault();
    if (email !== reEmail) {
      toast.error("Emails do not match!", { position: toast.POSITION.TOP_RIGHT });
      return;
    }
    try {
      const response = await fetch("/update", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code: 0, value: email }),
      });

      const result = await response.json();
      if (response.ok && result.success) {
        toast.success("Email updated successfully!", { position: toast.POSITION.TOP_RIGHT });
      } else {
        toast.error(result.error || "Failed to update email.", { position: toast.POSITION.TOP_RIGHT });
      }
    } catch (err) {
      toast.error("Error updating email. Please try again.", { position: toast.POSITION.TOP_RIGHT });
    }
  };

  const handlePasswordUpdate = async (e) => {
    e.preventDefault();
    if (password !== rePassword) {
      toast.error("Passwords do not match!", { position: toast.POSITION.TOP_RIGHT });
      return;
    }
    try {
      const response = await fetch("/update", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code: 1, value: password }),
      });

      const result = await response.json();
      if (response.ok && result.success) {
        toast.success("Password updated successfully!", { position: toast.POSITION.TOP_RIGHT });
      } else {
        toast.error(result.error || "Failed to update password.", { position: toast.POSITION.TOP_RIGHT });
      }
    } catch (err) {
      toast.error("Error updating password. Please try again.", { position: toast.POSITION.TOP_RIGHT });
    }
  };

  const handlePhoneUpdate = async (e) => {
    e.preventDefault();
    if (phone !== rePhone) {
      toast.error("Phone numbers do not match!", { position: toast.POSITION.TOP_RIGHT });
      return;
    }
    try {
      const response = await fetch("/update", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code: 2, value: phone }),
      });

      const result = await response.json();
      if (response.ok && result.success) {
        toast.success("Phone number updated successfully!", { position: toast.POSITION.TOP_RIGHT });
      } else {
        toast.error(result.error || "Failed to update phone number.", { position: toast.POSITION.TOP_RIGHT });
      }
    } catch (err) {
      toast.error("Error updating phone number. Please try again.", { position: toast.POSITION.TOP_RIGHT });
    }
  };

  const handleNotificationUpdate = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("/update", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code: 3, value: notification }),
      });

      const result = await response.json();
      if (response.ok && result.success) {
        toast.success("Notification method updated successfully!", { position: toast.POSITION.TOP_RIGHT });
      } else {
        toast.error(result.error || "Failed to update notification method.", { position: toast.POSITION.TOP_RIGHT });
      }
    } catch (err) {
      toast.error("Error updating notification method. Please try again.", { position: toast.POSITION.TOP_RIGHT });
    }
  };

  const handleAdminAccess = () => {
    if (isAdmin) {
      navigate("/admin");
    } else {
      toast.error("You do not have admin permissions.", {
        position: toast.POSITION.TOP_RIGHT,
      });
    }
  };

  return (
    <>
      <Header />
      <div className="preferences-container">
        <div className="preferences-box">
          <h2>Update Email</h2>
          <form onSubmit={handleEmailUpdate}>
            <label>
              Email
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </label>
            <label>
              Re-enter Email
              <input
                type="email"
                value={reEmail}
                onChange={(e) => setReEmail(e.target.value)}
                required
              />
            </label>
            <button type="submit">Update Email</button>
          </form>
        </div>
        <div className="preferences-box">
          <h2>Update Password</h2>
          <form onSubmit={handlePasswordUpdate}>
            <label>
              Password
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </label>
            <label>
              Re-enter Password
              <input
                type="password"
                value={rePassword}
                onChange={(e) => setRePassword(e.target.value)}
                required
              />
            </label>
            <button type="submit">Update Password</button>
          </form>
        </div>
        <div className="preferences-box">
          <h2>Update Phone Number</h2>
          <form onSubmit={handlePhoneUpdate}>
            <label>
              Phone Number
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                required
              />
            </label>
            <label>
              Re-enter Phone Number
              <input
                type="tel"
                value={rePhone}
                onChange={(e) => setRePhone(e.target.value)}
                required
              />
            </label>
            <button type="submit">Update Phone Number</button>
          </form>
        </div>
        <div className="preferences-box">
          <h2>Notification Settings</h2>
          <form onSubmit={handleNotificationUpdate}>
            <label>
              Notification
              <select
                value={notification}
                onChange={(e) => setNotification(e.target.value)}
              >
                <option value="Email">Email</option>
                <option value="Phone">Phone</option>
                <option value="off">Off</option>
              </select>
            </label>
            <button type="submit">Update Notification Settings</button>
          </form>
        </div>
        <div className="preferences-box">
          <h2>Admin Settings</h2>
          <button
            onClick={handleAdminAccess}
            disabled={!isAdmin}
            style={{
              backgroundColor: isAdmin ? "blue" : "gray",
              cursor: isAdmin ? "pointer" : "not-allowed",
              color: "#fff",
              padding: "10px 20px",
              border: "none",
              borderRadius: "5px",
            }}
          >
            Access Admin Settings
          </button>
        </div>
      </div>
      <ToastContainer />
    </>
  );
}

export default UserPreferences;
