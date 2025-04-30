import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Auth.css';

function Signup() {
  const [formData, setFormData] = useState(
      {
        username: '',
        password: '',
        hospital: '',
        doctorFirstName: '',
        doctorLastName: '',
        secret_key: '' });
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSignup = async e => {
    e.preventDefault();
    const response = await fetch('http://localhost:5000/api/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });
    const data = await response.json();
    setMessage(data.message);
    if (response.ok) {
      navigate('/login');
    }
  };

  return (
      <div className="auth-container">
        <h2>Hastane Kayıt</h2>
          <form onSubmit={handleSignup}>
              <input type="text" name="username" placeholder="Kullanıcı Adı" onChange={handleChange} required/>
              <input type="password" name="password" placeholder="Şifre" onChange={handleChange} required/>
              <input type="text" name="doctorFirstName" placeholder="Doktor Adı" onChange={handleChange} required/>
              <input type="text" name="doctorLastName" placeholder="Doktor Soyadı" onChange={handleChange} required/>
              <input type="text" name="hospital" placeholder="Hastane Adı" onChange={handleChange} required/>
              <input type="text" name="secret_key" placeholder="Kayıt Anahtarı" onChange={handleChange} required/>
              <button type="submit">Kayıt Ol</button>
              {message && <p className="message">{message}</p>}
          </form>
          <p className="switch-text">Zaten bir aboneliğiniz var mı? <span
              onClick={() => navigate('/login')}>Giriş Yapın</span></p>
      </div>
  );
}

export default Signup;
