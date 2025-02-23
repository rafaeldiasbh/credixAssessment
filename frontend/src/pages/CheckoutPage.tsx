import React, { useState } from 'react';
import { v5 as uuidv5 } from 'uuid';
import SHA256 from 'crypto-js/sha256';
import Modal from '../components/Modal';


interface Product {
  name: string;
  amount: number;
  unitcost: number;
}

interface Buyer {
  name: string;
  taxid: string;
  address: string;
  address2: string;
  postalcode: string;
  phone: string;
  email: string;
}

const CheckoutPage: React.FC = () => {
  const [buyerData, setBuyerData] = useState<Buyer>({
    name: 'RAFAEL GONCALVES DIAS',
    taxid: '26900161000125',
    address: 'R LAPINHA 741',
    address2: 'AP 505',
    postalcode: '01414905',
    phone: '551126883288',
    email: 'rafaelgdiasbh@gmail.com'
  });

  const [products, setProducts] = useState<Product[]>([]);
  const [newProduct, setNewProduct] = useState<Product>({ name: '', amount: 0, unitcost: 0 });
  const [discount, setDiscount] = useState<number>(0);
  const [freight, setFreight] = useState<number>(0);
  const [isDebugMode, setIsDebugMode] = useState<boolean>(false);
  const [paymentterm, setPaymentterm] = useState<string>('7');
  const [installments, setInstallments] = useState<number>(1);

  const [modalMessage, setModalMessage] = useState<string>('');
  const [showModal, setShowModal] = useState<boolean>(false);
  const [modalYesNo, setModalYesNo] = useState<boolean>(false);
  const [modalResolve, setModalResolve] = useState<((value: boolean) => void) | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const addProduct = () => {
    if (newProduct.name && (newProduct.amount||0) > 0 && (newProduct.unitcost||0) > 0) {
      setProducts([...products, newProduct]);
      setNewProduct({ name: '', amount: 0, unitcost: 0 });
    }
  };

  const calculateTotal = () => {
    const productsTotal = products.reduce((total, product) => total + (product.amount||0) * (product.unitcost||0), 0);
    return productsTotal - discount + freight;
  };

  const handleFinishOrder = async (idempotencyKey: string = '') => {
  setLoading(true); // Start loading
  
  const productsSum = products.reduce((total, product) => total + (product.amount||0) * (product.unitcost||0), 0).toFixed(2);
  const productstotal = { productstotal: productsSum };
  const total = { total: calculateTotal() };
  const body = { ...buyerData, ...productstotal, discount, freight, ...total, paymentterm, installments, products };
  
  if (!idempotencyKey)
    idempotencyKey = generateIdempotencyKey(JSON.stringify(body));

  try {
    const response = await fetchOrder(JSON.stringify(body), idempotencyKey);
    const payload = await response.json();

    if (response.status === 409) {
      showMessage("This purchase was already done. Are you sure to do it again?", true).then(yes => {
        if (yes) {
          idempotencyKey = generateIdempotencyKey(JSON.stringify(body) + `${Date.now()}`);
          handleFinishOrder(idempotencyKey);
        }
      });
    } else if (response.ok) {
      showMessage('Order successful with order ID: \n' + payload.credixid);
    } else {
      showMessage(payload.detail.data.message);
    }
  } catch (error) {
    console.error("Error handling the order:", error);
  } finally {
    setLoading(false); 
  }
};


  const fetchOrder = (body : string, idempotencyKey: string) => {
     return fetch("http://127.0.0.1:8000/api/v1/orders", {
      "method": "POST",  
      "headers": {
        "accept": "application/json",
        "content-type": "application/json",
        "Idempotency-Key": idempotencyKey,
      },
      "body": body
    });
  }

  const generateIdempotencyKey = (data: string): string => {
    // Hash the order data to create a consistent UUID
    const hash = SHA256(data).toString();
    return uuidv5(hash, uuidv5.URL);
  };

  const showMessage = (message: string, isYesNo: boolean = false): Promise<boolean> => {
    setModalYesNo(isYesNo);
    setModalMessage(message);
    setShowModal(true);

    return new Promise((resolve, reject) => {
      setModalResolve(() => (clickYes: boolean) => {
        setShowModal(false); 
        if (clickYes) resolve(true); // Resolve if "Yes" or "OK"
        else reject(false); // Reject if "No" (only for Yes/No mode)
      });
    });
  };

  //Handle modal promisses
  const handleModalConfirm = () => {
    if (modalResolve) modalResolve(true);
  };
  const handleModalCancel = () => {
    if (modalResolve) modalResolve(false);
  };

  return (
    <div className="flex flex-col h-full overflow-hidden"> {/* Full height, no overflow */}
      <div className="grid grid-cols-3 gap-4 p-4 flex-grow overflow-auto"> {/* Internal scrolling */}
        {/* Loading Indicator */}
        {loading && (
          <div className="absolute inset-0 flex justify-center items-center bg-gray-500 bg-opacity-50">
            <div className="text-white font-bold">Processing Order...</div>
          </div>
        )}
        
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
          <label className="block mb-2">Amount:</label>
          <input
            type="number"
            placeholder="Amount"
            value={newProduct.amount}
            onChange={(e) => setNewProduct({ ...newProduct, amount: Number(e.target.value) })}
            className="border p-2 mb-2 w-full"
          />
          <label className="block mb-2">Unit Cost:</label>
          <input
            type="number"
            placeholder="Unit Cost"
            value={newProduct.unitcost}
            onChange={(e) => setNewProduct({ ...newProduct, unitcost: Number(e.target.value) })}
            className="border p-2 mb-4 w-full"
          />
          <button onClick={addProduct} className="bg-blue-500 text-white p-2 rounded">Add Product</button>
        </div>

        {/* Right Section - Checkout Summary */}
        <div className="p-4 border rounded">
          <h2 className="text-xl font-bold mb-4">Checkout Summary</h2>

          <div className="mb-2">Products Total: ${products.reduce((total, product) => total + (product.amount||0) * (product.unitcost||0), 0).toFixed(2)}</div>

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

          <button onClick={() => handleFinishOrder('')} className="bg-green-500 text-white p-2 rounded">Finish Order</button>

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
            value={paymentterm}
            onChange={(e) => setPaymentterm(e.target.value)}
            className="border p-2 w-full mb-4"
          >
            <option value="7">7 Days</option>
            <option value="14">14 Days</option>
            <option value="30">30 Days</option>
          </select>

          <label className="block mb-2">Max Number of Installments:</label>
          <select
            value={installments}
            onChange={(e) => setInstallments(Number(e.target.value))}
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
                  <span>{product.amount} x ${product.unitcost?.toFixed(2)}</span>
                  <span className="font-bold">${((product.amount||0) * (product.unitcost||0)).toFixed(2)}</span>
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
          <label className="block mb-2">Name:</label>
          <input
            type="text"
            placeholder="Name"
            value={buyerData.name}
            onChange={(e) => setBuyerData({ ...buyerData, name: e.target.value })}
            className="border p-2 mb-2 w-full"
          />
          <label className="block mb-2">Tax Id:</label>
          <input
            type="text"
            placeholder="Tax Id"
            value={buyerData.taxid}
            onChange={(e) => setBuyerData({ ...buyerData, taxid: e.target.value })}
            className="border p-2 mb-2 w-full"
          />
          <label className="block mb-2">Address:</label>
          <input
            type="text"
            placeholder="Address"
            value={buyerData.address}
            onChange={(e) => setBuyerData({ ...buyerData, address: e.target.value })}
            className="border p-2 mb-2 w-full"
          />
          <label className="block mb-2">Address2:</label>
          <input
            type="text"
            placeholder="Address2"
            value={buyerData.address2}
            onChange={(e) => setBuyerData({ ...buyerData, address2: e.target.value })}
            className="border p-2 mb-2 w-full"
          />
          <label className="block mb-2">Postal Code:</label>
          <input
            type="text"
            placeholder="Postal Code"
            value={buyerData.postalcode}
            onChange={(e) => setBuyerData({ ...buyerData, postalcode: e.target.value })}
            className="border p-2 mb-2 w-full"
          />
          <label className="block mb-2">Phone:</label>
          <input
            type="text"
            placeholder="Phone (numbers only)"
            value={buyerData.phone}
            onChange={(e) => setBuyerData({ ...buyerData, phone: e.target.value })}
            className="border p-2 mb-2 w-full"
          />
          <label className="block mb-2">Email:</label>
          <input
            type="text"
            placeholder="Email"
            value={buyerData.email}
            onChange={(e) => setBuyerData({ ...buyerData, email: e.target.value })}
            className="border p-2 mb-2 w-full"
          />
        </div>
      </div>
      {/* Modal for duplicate request */}
      {showModal && (
        <Modal
          message={modalMessage}
          onConfirm={handleModalConfirm}
          onCancel={modalYesNo ? handleModalCancel : undefined} 
        />
      )}
    </div>
  );
};

export default CheckoutPage;