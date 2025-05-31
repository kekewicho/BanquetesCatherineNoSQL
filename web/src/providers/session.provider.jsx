import { createContext, useState, useEffect, useContext, useCallback } from 'react';
import { getCurrentUser as authGetCurrentUser, login as authLoginService, logout as authLogoutService } from '../services/auth.service';

const SessionContext = createContext(null);

export const SessionProvider = ({ children }) => {
    const [currentUser, setCurrentUser] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const user = authGetCurrentUser();
        if (user) {
            setCurrentUser(user);
        }
        setIsLoading(false);
    }, []);

    const login = useCallback(async (credentials) => {
        try {
            const user = await authLoginService(credentials);
            setCurrentUser(user);
            return user;
        } catch (error) {
            setCurrentUser(null);
            throw error;
        }
    }, []);

    const logout = useCallback(() => {
        authLogoutService();
        setCurrentUser(null);
    }, []);

    const value = {
        currentUser,
        isLoading,
        login,
        logout,
        isAuthenticated: !!currentUser 
    };

    return (
        <SessionContext.Provider value={value}>
            {children}
        </SessionContext.Provider>
    );
};

export const useSession = () => {
    const context = useContext(SessionContext);
    if (context === undefined || context === null) {
        throw new Error('useSession must be used within a SessionProvider');
    }
    return context;
};