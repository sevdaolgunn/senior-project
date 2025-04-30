import React from 'react';
import {BrowserRouter as Router, Routes, Route, Navigate} from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './components/Login';
import Signup from './components/Signup';
import MainPage from './components/MainPage';
import DoctorDashboard from './components/DoctorDashboard';

function PrivateRoute({ element }) {
  const { isLoggedIn } = useAuth();
  return isLoggedIn ? element : <Navigate to="/login" />;
}

function App() {
  return (
      <AuthProvider>
    <Router>
      <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
            <Route path="/dashboard" element={<PrivateRoute element={<DoctorDashboard />} />} />
          <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
          </AuthProvider>
  );
}

export default App;
