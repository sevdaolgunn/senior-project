import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './DoctorDashboard.css';

function DoctorDashboard({ doctorName = "Dr. Ayşe Yılmaz", hospitalName = "Acıbadem Hastanesi" }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div>
          <h2>Hoş geldiniz Dr. {user?.doctorFirstName} {user?.doctorLastName}</h2>
          <h4>{user?.hospital}</h4>
        </div>
        <button className="logout-btn" onClick={handleLogout}>Çıkış Yap</button>
      </header>

      <main className="dashboard-main">
        <section className="action-section">
          <h3>Asistan Paneli</h3>
          <p>Sesli semptom alımıyla hastalık tahmini başlatabilirsiniz.</p>
          <button className="start-btn">🎤 Sesli Analizi Başlat</button>
        </section>

        <section className="history-section">
          <h4>Son Teşhisler</h4>
          <ul>
            <li>👤 Mehmet Y. - Grip</li>
            <li>👤 Elif A. - Migren</li>
            <li>👤 Ahmet K. - Bronşit</li>
          </ul>
        </section>
      </main>
    </div>
  );
}


export default DoctorDashboard;
