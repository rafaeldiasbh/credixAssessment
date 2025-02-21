import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import CheckoutPage from './pages/CheckoutPage';
import OrdersPage from './pages/OrdersPage';

const App: React.FC = () => {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <div className="flex-grow p-4 overflow-hidden" style={{ height: 'calc(100vh - 4rem)' }}> {/* Adjust for Navbar height */}
          <Routes>
            <Route path="/" element={<CheckoutPage />} />
            <Route path="/orders" element={<OrdersPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;