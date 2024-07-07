import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import Papa from 'papaparse';
import FilterOptions from '../components/FilterOptions';

const HeatMap = dynamic(() => import('../components/HeatMap'), { ssr: false });
const LineChart = dynamic(() => import('../components/LineChart'), { ssr: false });

export default function Home() {
  const [data, setData] = useState([]);
  const [filters, setFilters] = useState({
    state: 'All',
    district: 'All',
    commodity: 'All'
  });
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
    fetch('/api/data')
      .then(response => response.json())
      .then(data => {
        console.log(data);
        setData(data);
      });
  }, []);

  const fetchData = () => {
    Papa.parse('/data.csv', {
      download: true,
      header: true,
      complete: (results) => {
        setData(results.data);
      },
    });
  };

  if (!isClient) return null;

  return (
    <div>
      <h1>Agricultural Market Dashboard</h1>
      <FilterOptions data={data} filters={filters} setFilters={setFilters} />
      <HeatMap data={data} filters={filters} />
      <LineChart data={data} filters={filters} />
    </div>
  );
}