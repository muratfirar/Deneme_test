import React, { useState, useEffect } from 'react';

const App = () => {
  const [firms, setFirms] = useState([]);
  const [newFirm, setNewFirm] = useState({
    name: '',
    vkn: '',
    establishment_date: '',
    firm_type: '',
    address: '',
  });

  useEffect(() => {
    fetch('/api/firms')
      .then((res) => res.json())
      .then((data) => setFirms(data));
  }, []);

  const handleChange = (e) => {
    setNewFirm({ ...newFirm, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch('/api/firms', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newFirm),
    })
      .then((res) => res.json())
      .then(() => {
        setNewFirm({ name: '', vkn: '', establishment_date: '', firm_type: '', address: '' });
        fetch('/api/firms')
          .then((res) => res.json())
          .then((data) => setFirms(data));
      });
  };

  return (
    <div>
      <h1>Firm Management</h1>
      <form onSubmit={handleSubmit}>
        <input name="name" placeholder="Firm Name" value={newFirm.name} onChange={handleChange} required />
        <input name="vkn" placeholder="VKN" value={newFirm.vkn} onChange={handleChange} required />
        <input name="establishment_date" placeholder="Establishment Date" value={newFirm.establishment_date} onChange={handleChange} required />
        <input name="firm_type" placeholder="Firm Type" value={newFirm.firm_type} onChange={handleChange} required />
        <input name="address" placeholder="Address" value={newFirm.address} onChange={handleChange} />
        <button type="submit">Add Firm</button>
      </form>
      <ul>
        {firms.map((firm) => (
          <li key={firm.id}>
            {firm.name} ({firm.vkn})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default App;
