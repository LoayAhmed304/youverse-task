import React, { useState } from 'react';

const CourseBlock = ({ handleGetCourse, itemDetails }) => {
  const [itemId, setItemId] = useState('');

  return (
    <div className="bg-white h-full items-center justify-center rounded shadow p-6 w-full max-w-md flex flex-col gap-4">
      <h2 className="text-xl font-semibold">Get Course details by ID</h2>
      <h4 className="text-gray-600">
        You must be enrolled to that course or the owner of it
      </h4>
      <p className="text-gray-400 mb-4 text-center">
        Returns the videos details for that course (not the playback stream)
      </p>
      <form
        className="flex gap-2 items-center"
        onSubmit={(e) => e.preventDefault()}
      >
        <input
          type="text"
          placeholder="Enter ID"
          className="border rounded px-3 py-2 flex-1"
          value={itemId}
          onChange={(e) => setItemId(e.target.value)}
        />
        <button
          className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600 cursor-pointer transition-colors"
          type="button"
          onClick={(e) => handleGetCourse(e, itemId)}
        >
          Get Details
        </button>
      </form>
      {itemDetails?.map((item) => (
        <li key={item.id}>
          <div className="border-b py-2">
            <h3 className="text-lg font-semibold">{item.title}</h3>
            <p>duration: {item.description}</p>
            <p>Asset ID: {item.asset_id}</p>
            <p>Category: {item.category}</p>
            <p>Description: {item.description}</p>
          </div>
        </li>
      ))}
    </div>
  );
};
export default CourseBlock;
