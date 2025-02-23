import React from 'react';

interface ModalProps {
  message: string; // The message to display
  onConfirm: () => void; // Callback for the "Yes" or "OK" button
  onCancel?: () => void; // Optional callback for the "No" button
}

const Modal: React.FC<ModalProps> = ({ message, onConfirm, onCancel }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg">
        <h2 className="text-xl font-bold mb-4">Notification</h2>
        <p>{message}</p>
        <div className="mt-4 flex justify-end">
          {onCancel && ( // Show "No" button only if onCancel is provided
            <button
              onClick={onCancel}
              className="bg-gray-500 text-white p-2 rounded mr-2"
            >
              No
            </button>
          )}
          <button
            onClick={onConfirm}
            className="bg-green-500 text-white p-2 rounded"
          >
            {onCancel ? 'Yes' : 'OK'} {/* Show "Yes" or "OK" based on mode */}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Modal;