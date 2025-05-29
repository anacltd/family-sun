import './SunburstControls.css';

const SunburstControls = ({
  generations,
  setGenerations,
  palette,
  setPalette,
  colorBy,
  setColorBy,
  isSidebarOpen
}) => {
  return (
    <div className="sunburst-controls">
      <div className="form-group control-item">
        
        {isSidebarOpen && (
          <div className="control-content">
            <label htmlFor="generations">Number of generations to display:</label>
            <input
              id="generations"
              type="number"
              value={generations}
              onChange={(e) => setGenerations(Number(e.target.value))}
              min="1"
              max="20"
            />
          </div>
        )}
      </div>

      <div className="form-group control-item">
        
        {isSidebarOpen && (
          <div className="control-content">
            <label htmlFor="colorBy">Color family tree by:</label>
            <select
              id="colorBy"
              value={colorBy}
              onChange={(e) => setColorBy(e.target.value)}
            >
              <option value="generation">Generation</option>
              <option value="patronym">Patronym</option>
              <option value="department">Department</option>
              <option value="region">Region</option>
            </select>
          </div>
        )}
      </div>

      <div className="form-group control-item">
        
        {isSidebarOpen && (
          <div className="control-content">
            <label htmlFor="palette">Color palette:</label>
            <select
              id="palette"
              value={palette}
              onChange={(e) => setPalette(e.target.value)}
            >
              <option value="earth">Earth</option>
              <option value="vintage">Vintage</option>
              <option value="soft_rainbow">Soft Rainbow</option>
              <option value="warm">Warm</option>
              <option value="moss">Moss</option>
              <option value="clay">Clay</option>
            </select>
          </div>
        )}
      </div>
    </div>
  );
};

export default SunburstControls;