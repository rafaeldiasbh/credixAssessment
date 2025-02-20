import React, { useState } from 'react';

interface Product {
  name: string;
  amount?: number;
  unitCost?: number;
}

const CheckoutPage: React.FC = () => {
  const [buyerData, setBuyerData] = useState({
    name: '',
    id: '',
    address: '',
    zipCode: '',
    phone: ''
  });

  const [products, setProducts] = useState<Product[]>([]);
  const [newProduct, setNewProduct] = useState<Product>({ name: '', amount: undefined, unitCost: undefined });
  const [discount, setDiscount] = useState<number>(0);
  const [freight, setFreight] = useState<number>(0);
  const [isDebugMode, setIsDebugMode] = useState<boolean>(false);
  const [paymentTerm, setPaymentTerm] = useState<string>('7 days');
  const [maxInstallments, setMaxInstallments] = useState<number>(1);

  const addProduct = () => {
    if (newProduct.name && newProduct.amount > 0 && newProduct.unitCost > 0) {
      setProducts([...products, newProduct]);
      setNewProduct({ name: '', amount: undefined, unitCost: undefined });
    }
  };

  const calculateTotal = () => {
    const productsTotal = products.reduce((total, product) => total + product.amount * product.unitCost, 0);
    return productsTotal - discount + freight;
  };

  const handleFinishOrder = () => {
    window.location.href = '/invoice';
  };

  return (
    <div className="grid grid-cols-3 gap-4 p-4">
      {/* Left Section - Product Inputs */}
      <div className="col-span-2 p-4 border rounded">
        <h2 className="text-xl font-bold mb-4">Add Product</h2>
        <input
          type="text"
          placeholder="Product Name"
          value={newProduct.name}
          onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
          className="border p-2 mb-2 w-full"
        />
        <input
          type="number"
          placeholder="Amount"
          value={newProduct.amount}
          onChange={(e) => setNewProduct({ ...newProduct, amount: Number(e.target.value) })}
          className="border p-2 mb-2 w-full"
        />
        <input
          type="number"
          placeholder="Unit Cost"
          value={newProduct.unitCost}
          onChange={(e) => setNewProduct({ ...newProduct, unitCost: Number(e.target.value) })}
          className="border p-2 mb-4 w-full"
        />
        <button onClick={addProduct} className="bg-blue-500 text-white p-2 rounded">Add Product</button>
      </div>

      {/* Right Section - Checkout Summary */}
      <div className="p-4 border rounded">
        <h2 className="text-xl font-bold mb-4">Checkout Summary</h2>

        <div className="mb-2">Products Total: ${products.reduce((total, product) => total + product.amount * product.unitCost, 0).toFixed(2)}</div>

        <div className="mb-2">
          Discount: 
          {isDebugMode ? (
            <input
              type="number"
              value={discount}
              onChange={(e) => setDiscount(Number(e.target.value))}
              className="border p-1 ml-2"
            />
          ) : (
            `$${discount.toFixed(2)}`
          )}
        </div>

        <div className="mb-2">
          Delivery Cost/Freight: 
          {isDebugMode ? (
            <input
              type="number"
              value={freight}
              onChange={(e) => setFreight(Number(e.target.value))}
              className="border p-1 ml-2"
            />
          ) : (
            `$${freight.toFixed(2)}`
          )}
        </div>

        <div className="mb-4 font-bold">Total: ${calculateTotal().toFixed(2)}</div>

        <button onClick={handleFinishOrder} className="bg-green-500 text-white p-2 rounded">Finish Order</button>

        <div className="mt-4">
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={isDebugMode}
              onChange={() => setIsDebugMode(!isDebugMode)}
              className="mr-2"
            />
            Enable Debug Mode
          </label>
        </div>
      </div>      

      {/* Left Section - Payment Options */}
      <div className="col-span-2 p-4 border rounded mt-4">
        <h2 className="text-xl font-bold mb-4">Payment Options</h2>
        <label className="block mb-2">Payment Term:</label>
        <select
          value={paymentTerm}
          onChange={(e) => setPaymentTerm(e.target.value)}
          className="border p-2 w-full mb-4"
        >
          <option value="7 days">7 Days</option>
          <option value="14 days">14 Days</option>
          <option value="30 days">30 Days</option>
        </select>

        <label className="block mb-2">Max Number of Installments:</label>
        <select
          value={maxInstallments}
          onChange={(e) => setMaxInstallments(Number(e.target.value))}
          className="border p-2 w-full"
        >
          {[...Array(12).keys()].map((i) => (
            <option key={i + 1} value={i + 1}>{i + 1}</option>
          ))}
        </select>
      </div>

      {/* Middle Section - Product List */}
      <div className="row-span-2 p-4 border rounded mt-4">
        <h2 className="text-xl font-bold mb-4">Product List</h2>
        {products.length > 0 ? (
          <div className="space-y-2">
            {products.map((product, index) => (
              <div key={index} className="flex justify-between items-center border p-2 rounded">
                <span>{product.name}</span>
                <span>{product.amount} x ${product.unitCost?.toFixed(2)}</span>
                <span className="font-bold">${(product.amount * product.unitCost).toFixed(2)}</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No products added yet.</p>
        )}
      </div>
      
      {/* Left Section - Buyer Data */}
      <div className="col-span-2 p-4 border rounded mb-4">
        <h2 className="text-xl font-bold mb-4">Buyer Information</h2>
        <input
          type="text"
          placeholder="Name"
          value={buyerData.name}
          onChange={(e) => setBuyerData({ ...buyerData, name: e.target.value })}
          className="border p-2 mb-2 w-full"
        />
        <input
          type="text"
          placeholder="ID"
          value={buyerData.id}
          onChange={(e) => setBuyerData({ ...buyerData, id: e.target.value })}
          className="border p-2 mb-2 w-full"
        />
        <input
          type="text"
          placeholder="Address"
          value={buyerData.address}
          onChange={(e) => setBuyerData({ ...buyerData, address: e.target.value })}
          className="border p-2 mb-2 w-full"
        />
        <input
          type="text"
          placeholder="Zip Code"
          value={buyerData.zipCode}
          onChange={(e) => setBuyerData({ ...buyerData, zipCode: e.target.value })}
          className="border p-2 mb-2 w-full"
        />
        <input
          type="text"
          placeholder="Phone"
          value={buyerData.phone}
          onChange={(e) => setBuyerData({ ...buyerData, phone: e.target.value })}
          className="border p-2 mb-2 w-full"
        />
      </div>
    </div>
  );
};

export default CheckoutPage;

// Invoice Page
const InvoicePage: React.FC = () => {
  const [isSuccess, setIsSuccess] = useState(false);

  const handleRealFinishOrder = () => {
    // Mock backend call
    setTimeout(() => {
      setIsSuccess(true);
    }, 1000);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Invoice</h1>
      <p>Product details, totals, taxes, and other information go here.</p>
      <button onClick={handleRealFinishOrder} className="bg-blue-500 text-white p-2 rounded mt-4">Finish Order</button>

      {isSuccess && (
        <div className="mt-4 p-4 bg-green-100 border border-green-500 text-green-700 rounded">
          Order completed successfully!
        </div>
      )}
    </div>
  );
};

export { InvoicePage };