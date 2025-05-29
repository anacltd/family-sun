import { useState, useCallback } from 'react';
import Sidebar from './Sidebar';
import ChartArea from './ChartArea';
import './App.css';


function App() {
  const [generations, setGenerations] = useState(3);
  const [colorBy, setColorBy] = useState('generation');
  const [palette, setPalette] = useState('pastel');
  const [selectedFile, setSelectedFile] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [plotlyNode, setPlotlyNode] = useState(null);

  const handleFileChange = (e) => setSelectedFile(e.target.files[0]);

  const handleGenerateClick = async () => {
    if (!selectedFile) return alert('Please select a GEDCOM file first.');
    setIsSidebarOpen(false);

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('nb_of_generations', generations);
    formData.append('color_by', colorBy);
    formData.append('palette', palette);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error(`Upload failed: ${response.status}`);
      const result = await response.json();
      setChartData(result.data);
    } catch (error) {
      console.error('Upload error:', error);
      alert('Failed to upload and generate chart');
    }
  };

  const storePlotlyNode = useCallback((node) => {
      setPlotlyNode(node);
  }, []);

  const handleDownloadClick = async () => {
    if (!chartData) {
        alert("No chart data to download.");
        return;
    }

    try {
      const dataUrl = await Plotly.toImage(plotlyNode, {
        format: 'svg',
        width: 1200,
        height: 800,
        scale: 2
      });

      const link = document.createElement('a');
      link.href = dataUrl;
      link.download = 'family-tree-chart.svg';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Failed to download chart:', error);
      alert('Failed to download chart. See console for details.');
    }
  };

  return (
    <div className="app-container">
      <Sidebar
        isOpen={isSidebarOpen}
        toggle={() => setIsSidebarOpen(!isSidebarOpen)}
        generations={generations}
        setGenerations={setGenerations}
        colorBy={colorBy}
        setColorBy={setColorBy}
        palette={palette}
        setPalette={setPalette}
        selectedFile={selectedFile}
        onFileChange={handleFileChange}
        onGenerate={handleGenerateClick}
        onDownload={handleDownloadClick}
        chartData={chartData}
      />
      <ChartArea
        chartData={chartData}
        palette={palette}
        isSidebarOpen={isSidebarOpen}
        setPlotlyNodeReference={storePlotlyNode}
      />
    </div>
  );
}

export default App;