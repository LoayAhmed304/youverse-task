import React, { useState } from 'react';
import axios from 'axios';

const LoginBlock = ({ handleLogin, handleSignup, loginResult }) => {
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');

  return (
    <div>
      <div className="bg-white rounded shadow p-6 w-full max-w-md h-full flex flex-col gap-4 justify-center">
        <h2 className="text-xl text-center font-semibold mb-2">
          Login / Signup
        </h2>
        <form
          className="flex flex-col gap-2"
          onSubmit={(e) => e.preventDefault()}
        >
          <input
            type="email"
            placeholder="Email"
            className="border rounded px-3 py-2"
            value={loginEmail}
            onChange={(e) => setLoginEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            className="border rounded px-3 py-2"
            value={loginPassword}
            onChange={(e) => setLoginPassword(e.target.value)}
          />
          <div className="flex justify-center gap-2 mt-2">
            <button
              className="bg-blue-500 text-white px-4 py-2 rounded"
              type="button"
              onClick={() => handleLogin(loginEmail, loginPassword)}
            >
              Login
            </button>
            <button
              className="bg-green-500 text-white px-4 py-2 rounded"
              type="button"
              onClick={() => handleSignup(loginEmail, loginPassword)}
            >
              Signup
            </button>
          </div>
        </form>
        {loginResult && (
          <div className="mt-2 text-green-700">{loginResult}</div>
        )}
      </div>
    </div>
  );
};

export default LoginBlock;
