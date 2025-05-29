// Sidebar.jsx
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa';
import SunburstControls from './SunburstControls';
import './Sidebar.css';

function Sidebar({
  isOpen,
  toggle,
  generations,
  setGenerations,
  colorBy,
  setColorBy,
  palette,
  setPalette,
  selectedFile,
  onFileChange,
  onGenerate,
  onDownload,
  chartData
}) {
  const displayFileName = selectedFile ? selectedFile.name : "Choose a GEDCOM file";

  return (
    <div className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
      <div className="sidebar-toggle" onClick={toggle}>
        {isOpen ? <FaChevronLeft /> : <FaChevronRight />}
      </div>

      <div className="sidebar-section">
        <SunburstControls
          generations={generations}
          setGenerations={setGenerations}
          palette={palette}
          setPalette={setPalette}
          colorBy={colorBy}
          setColorBy={setColorBy}
          isSidebarOpen={isOpen}
        />
      </div>

      {isOpen && (
        <>
          <div className="sidebar-section upload-section">
            <label htmlFor="file-upload" className="custom-file-upload">
              {displayFileName}
            </label>
            <input id="file-upload" type="file" onChange={onFileChange} />
          </div>

          <div className="sidebar-section">
            <button className="generate-button" onClick={onGenerate}>
              Generate Family Tree
            </button>
          </div>

          {chartData && (
            <div className="sidebar-section">
              <button className="generate-button download-button" onClick={onDownload}>
                Download
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default Sidebar;