import React, { useState } from 'react';

const CreateVideo = ({ handleCreateVideo }) => {
  const [uploading, setUploading] = useState(false);
  const [videoData, setVideoData] = useState({
    title: '',
    description: '',
    course_id: '',
    duration: '',
    category: '',
    subcategory: '',
    file: null,
  });

  const handleChange = (e) => {
    const { name, value, type, files } = e.target;
    if (type === 'file') {
      setVideoData({ ...videoData, [name]: files[0] });
    } else {
      setVideoData({ ...videoData, [name]: value });
    }
  };

  return (
    <div>
      <div className="bg-white rounded shadow p-6 w-full max-w-md h-full items-center justify-center flex flex-col gap-4">
        <h2 className="text-xl font-semibold mb-2">Create Video</h2>
        <form
          className="flex flex-col gap-2"
          onSubmit={(e) => e.preventDefault()}
        >
          <input
            type="text"
            name="title"
            placeholder="Title"
            className="border rounded px-3 py-2 flex-1"
            value={videoData.title}
            onChange={handleChange}
          />
          <input
            type="text"
            name="description"
            placeholder="Description"
            className="border rounded px-3 py-2 flex-1"
            value={videoData.description}
            onChange={handleChange}
          />
          <input
            type="text"
            name="course_id"
            placeholder="Course ID"
            className="border rounded px-3 py-2 flex-1"
            value={videoData.course_id}
            onChange={handleChange}
          />
          <input
            type="file"
            name="file"
            accept="video/mp4"
            className="border rounded px-3 py-2 flex-1"
            onChange={handleChange}
          />
          <input
            type="text"
            name="duration"
            placeholder="Duration in seconds (e.g. 120)"
            className="border rounded px-3 py-2 flex-1"
            value={videoData.duration}
            onChange={handleChange}
          />
          <input
            type="text"
            name="category"
            placeholder="Category"
            className="border rounded px-3 py-2 flex-1"
            value={videoData.category}
            onChange={handleChange}
          />
          <input
            type="text"
            name="subcategory"
            placeholder="Subcategory"
            className="border rounded px-3 py-2 flex-1"
            value={videoData.subcategory}
            onChange={handleChange}
          />
          <button
            className="bg-purple-500 text-white px-4 py-2 rounded"
            type="button"
            onClick={(e) => handleCreateVideo(e, videoData, setUploading)}
          >
            {uploading ? 'Uploading...' : 'Create Video'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreateVideo;
