import React from 'react';
import { useNavigate } from 'react-router-dom';
import './MainPage.css';

function MainPage() {
  const navigate = useNavigate();

  return (
    <div className="main-container">
      <div className="main-content">
        <h1>🏥 Dijital Hastane Paneline Hoş Geldiniz</h1>
        <p>Lütfen giriş yapın veya yeni bir hesap oluşturun.</p>
        <div className="main-buttons">
          <button onClick={() => navigate('/login')}>Giriş Yap</button>
          <button onClick={() => navigate('/signup')}>Kayıt Ol</button>
        </div>
      </div>
    </div>
  );
}

export default MainPage;
