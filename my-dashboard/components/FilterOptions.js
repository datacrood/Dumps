import { useEffect, useState } from 'react';

export default function FilterOptions({ data, filters, setFilters }) {
  const [options, setOptions] = useState({
    states: ['All'],
    districts: ['All'],
    commodities: ['All']
  });

  useEffect(() => {
    if (data.length > 0) {
      setOptions({
        states: ['All', ...new Set(data.map(item => item.census_state_name))],
        districts: ['All', ...new Set(data.map(item => item.census_district_name))],
        commodities: ['All', ...new Set(data.map(item => item.commodity_name))]
      });
    }
  }, [data]);

  useEffect(() => {
    console.log(options); // Log options to verify
  }, [options]);

  useEffect(() => {
    // Update districts based on selected state
    if (filters.state && filters.state !== 'All') {
      const districts = data.filter(item => item.census_state_name === filters.state)
                            .map(item => item.census_district_name);
      setOptions(prevOptions => ({
        ...prevOptions,
        districts: ['All', ...new Set(districts)]
      }));
    } else {
      setOptions(prevOptions => ({
        ...prevOptions,
        districts: ['All']
      }));
    }
  }, [filters.state, data]);

  

  const handleChange = (e, filterType) => {
    setFilters(prev => ({ ...prev, [filterType]: e.target.value }));
  };

  return (
    <div>
      <select value={filters.state} onChange={e => handleChange(e, 'state')}>
        {options.states.map(state => <option key={state} value={state}>{state}</option>)}
      </select>
      <select value={filters.district} onChange={e => handleChange(e, 'district')}>
        {options.districts.map(district => <option key={district} value={district}>{district}</option>)}
      </select>
      <select value={filters.commodity} onChange={e => handleChange(e, 'commodity')}>
        {options.commodities.map(commodity => <option key={commodity} value={commodity}>{commodity}</option>)}
      </select>
    </div>
  );
}