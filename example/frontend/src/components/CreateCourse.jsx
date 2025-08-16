import React from 'react';

const CreateCourse = ({ handleCreateCourse }) => {
  const [courseData, setCourseData] = React.useState({
    name: '',
    description: '',
    category: '',
  });
  return (
    <div>
      <div className="bg-white rounded shadow p-6 w-full h-full items-center justify-center max-w-md flex flex-col gap-4">
        <h2 className="text-xl font-semibold mb-2">Create Course</h2>
        <h4 className="text-gray-600 mb-4">
          Make sure the course name is not already in use
        </h4>
        <form
          className="flex flex-col gap-2 items-center"
          onSubmit={(e) => e.preventDefault()}
        >
          <input
            type="text"
            placeholder="Enter Name"
            className="border rounded px-3 py-2 flex-1"
            value={courseData.name}
            onChange={(e) =>
              setCourseData({ ...courseData, name: e.target.value })
            }
          />
          <input
            type="text"
            placeholder="Enter Description"
            className="border rounded px-3 py-2 flex-1"
            value={courseData.description}
            onChange={(e) =>
              setCourseData({ ...courseData, description: e.target.value })
            }
          />
          <input
            type="text"
            placeholder="Enter Category"
            className="border rounded px-3 py-2 flex-1"
            value={courseData.category}
            onChange={(e) =>
              setCourseData({ ...courseData, category: e.target.value })
            }
          />

          <button
            className="bg-purple-500 text-white px-4 py-2 rounded mt-4 hover:bg-purple-600 cursor-pointer transition-colors"
            type="button"
            onClick={(e) => handleCreateCourse(e, courseData)}
          >
            Create Course
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreateCourse;
