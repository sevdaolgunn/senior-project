import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './Auth.css';

function Login() {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const { login } = useAuth(); // Auth context'ten login fonksiyonunu aldık

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleLogin = async e => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      const data = await response.json();
      setMessage(data.message);

      if (response.ok) {
        login({
           username: data.username,
           doctorFirstName: data.doctorFirstName,
           doctorLastName: data.doctorLastName,
           hospital: data.hospital
        }); // Giriş durumu context'e yazılır
        navigate('/dashboard'); // Dashboard sayfasına yönlendirilir
      }
    } catch (error) {
      console.error('Giriş hatası:', error);
      setMessage('Sunucu hatası.');
    }
  };

  return (
    <div className="auth-container">
      <h2>Hastane Giriş</h2>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          name="username"
          placeholder="Kullanıcı Adı"
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Şifre"
          onChange={handleChange}
          required
        />
        <button type="submit">Giriş Yap</button>
        {message && <p className="message">{message}</p>}
      </form>
      <p className="switch-text">
        Hesabınız yok mu?{' '}
        <span onClick={() => navigate('/signup')}>Kayıt Olun</span>
      </p>
    </div>
  );
}

export default Login;
