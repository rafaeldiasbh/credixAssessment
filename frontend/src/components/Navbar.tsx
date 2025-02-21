import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
  return (
    <nav className="bg-blue-500 p-4 text-white">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold">My Store</h1>
        <div className="space-x-4">
          <Link to="/" className="hover:underline">Checkout</Link>
          <Link to="/orders" className="hover:underline">Orders</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;