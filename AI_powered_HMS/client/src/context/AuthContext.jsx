import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('kaire_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [token, setToken] = useState(() => localStorage.getItem('kaire_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const verifyUser = async () => {
      const storedToken = localStorage.getItem('kaire_token');
      if (storedToken) {
        try {
          const res = await authService.getMe();
          if (res.success && res.user) {
            setUser(res.user);
            localStorage.setItem('kaire_user', JSON.stringify(res.user));
          }
        } catch (err) {
          console.warn("Session restore failed, maintaining offline token context:", err.message);
        }
      }
      setLoading(false);
    };
    verifyUser();
  }, []);

  const login = async (email, password) => {
    const res = await authService.login({ email, password });
    if (res.success && res.token) {
      setToken(res.token);
      setUser(res.user);
      localStorage.setItem('kaire_token', res.token);
      localStorage.setItem('kaire_user', JSON.stringify(res.user));
      return res.user;
    }
    throw new Error(res.message || 'Login failed');
  };

  const quickSwitch = async (targetRole) => {
    try {
      const res = await authService.quickLogin(targetRole);
      if (res.success && res.token) {
        setToken(res.token);
        setUser(res.user);
        localStorage.setItem('kaire_token', res.token);
        localStorage.setItem('kaire_user', JSON.stringify(res.user));
        return res.user;
      }
    } catch (err) {
      console.error("Quick switch error:", err);
      // Fallback mock session for instant UI review
      const mockUsers = {
        admin: { id: 1, full_name: 'Kailash Admin', role: 'admin', email: 'admin@kairehealth.com', first_name: 'Kailash', last_name: 'Admin', avatar_url: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150' },
        doctor: { id: 2, full_name: 'Dr. Ankit', role: 'doctor', email: 'dr.ankit@kairehealth.com', first_name: 'Ankit', last_name: 'Kumar', avatar_url: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150' },
        doctor_sarah: { id: 2, full_name: 'Dr. Ankit', role: 'doctor', email: 'dr.ankit@kairehealth.com', first_name: 'Ankit', last_name: 'Kumar', avatar_url: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150' },
        doctor_alex: { id: 3, full_name: 'Dr. Rawtaram', role: 'doctor', email: 'dr.rawtaram@kairehealth.com', first_name: 'Rawtaram', last_name: 'Choudhary', avatar_url: 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=150' },
        doctor_elena: { id: 4, full_name: 'Dr. Amit', role: 'doctor', email: 'dr.amit@kairehealth.com', first_name: 'Amit', last_name: 'Sharma', avatar_url: 'https://images.unsplash.com/photo-1594824813689-f53e6b72a0f8?w=150' },
        nurse: { id: 5, full_name: 'Nurse Sunder', role: 'nurse', email: 'nurse.sunder@kairehealth.com', first_name: 'Sunder', last_name: 'Singh', avatar_url: 'https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=150' },
        nurse_emily: { id: 5, full_name: 'Nurse Sunder', role: 'nurse', email: 'nurse.sunder@kairehealth.com', first_name: 'Sunder', last_name: 'Singh', avatar_url: 'https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=150' },
        nurse_marcus: { id: 6, full_name: 'Nurse Dholi', role: 'nurse', email: 'nurse.dholi@kairehealth.com', first_name: 'Dholi', last_name: 'Devi', avatar_url: 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=150' },
        patient: { id: 7, full_name: 'Mukesh', role: 'patient', email: 'mukesh@gmail.com', first_name: 'Mukesh', last_name: 'Sharma', avatar_url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150' },
        patient_john: { id: 7, full_name: 'Mukesh', role: 'patient', email: 'mukesh@gmail.com', first_name: 'Mukesh', last_name: 'Sharma', avatar_url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150' },
        patient_maria: { id: 8, full_name: 'Yanshu', role: 'patient', email: 'yanshu@gmail.com', first_name: 'Yanshu', last_name: 'Verma', avatar_url: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150' },
        patient_robert: { id: 9, full_name: 'Robert Chen', role: 'patient', email: 'robert.chen@gmail.com', first_name: 'Robert', last_name: 'Chen', avatar_url: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150' },
        patient_aisha: { id: 10, full_name: 'Aisha Patel', role: 'patient', email: 'aisha.patel@gmail.com', first_name: 'Aisha', last_name: 'Patel', avatar_url: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150' }
      };
      const mockU = mockUsers[targetRole] || mockUsers[targetRole.split('_')[0]] || mockUsers.admin;
      setUser(mockU);
      localStorage.setItem('kaire_user', JSON.stringify(mockU));
      return mockU;
    }
  };

  const register = async (userData) => {
    const res = await authService.register(userData);
    if (res.success && res.token) {
      setToken(res.token);
      setUser(res.user);
      localStorage.setItem('kaire_token', res.token);
      localStorage.setItem('kaire_user', JSON.stringify(res.user));
      return res.user;
    }
    throw new Error(res.message || 'Registration failed');
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('kaire_token');
    localStorage.removeItem('kaire_user');
  };

  return (
    <AuthContext.Provider value={{
      user,
      token,
      loading,
      isAuthenticated: !!user,
      role: user?.role || null,
      login,
      quickSwitch,
      register,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
