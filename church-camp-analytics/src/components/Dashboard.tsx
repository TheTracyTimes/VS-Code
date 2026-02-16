import React from 'react';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import type { AnalyticsData } from '../types';
import './Dashboard.css';

interface DashboardProps {
  analytics: AnalyticsData;
}

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#fee140', '#30cfd0'];

const Dashboard: React.FC<DashboardProps> = ({ analytics }) => {
  // Convert analytics data to chart-friendly format
  const ageData = Object.entries(analytics.ageDistribution).map(([range, count]) => ({
    range,
    count,
  }));

  const genderData = Object.entries(analytics.genderDistribution).map(([name, value]) => ({
    name,
    value,
  }));

  const nationalityData = Object.entries(analytics.nationalityDistribution).map(([name, value]) => ({
    name,
    value,
  }));

  const assemblyData = Object.entries(analytics.assemblyDistribution)
    .map(([name, value]) => ({
      name: name.length > 40 ? name.substring(0, 40) + '...' : name,
      fullName: name,
      value
    }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 10);

  const transportationData = Object.entries(analytics.transportationStats).map(([name, value]) => ({
    name,
    value,
  }));

  const allergyData = Object.entries(analytics.allergyStats).map(([name, value]) => ({
    name,
    value,
  }));

  const paymentData = Object.entries(analytics.paymentOptionStats).map(([name, value]) => ({
    name,
    value,
  }));

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Church Camp Registration Analytics Dashboard</h2>
        <p className="dashboard-subtitle">Real-time insights for planning and organization</p>
      </div>

      {/* Key Metrics Cards */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon">👥</div>
          <div className="metric-content">
            <h3>Total Registrations</h3>
            <p className="metric-value">{analytics.totalRegistrations}</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">🎂</div>
          <div className="metric-content">
            <h3>Average Age</h3>
            <p className="metric-value">{analytics.averageAge} years</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">👨‍👩‍👧</div>
          <div className="metric-content">
            <h3>Minors (Under 18)</h3>
            <p className="metric-value">{analytics.minorsRequiringChaperone}</p>
            <p className="metric-subtitle">
              {analytics.totalRegistrations > 0
                ? `${Math.round((analytics.minorsRequiringChaperone / analytics.totalRegistrations) * 100)}%`
                : '0%'}{' '}
              require chaperone
            </p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">⛪</div>
          <div className="metric-content">
            <h3>Assemblies</h3>
            <p className="metric-value">{Object.keys(analytics.assemblyDistribution).length}</p>
            <p className="metric-subtitle">Participating churches</p>
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="charts-grid">
        {/* Age Distribution */}
        <div className="chart-card">
          <h3>Age Distribution</h3>
          <p className="chart-description">Understanding our demographic spread</p>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={ageData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="range" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#667eea" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Gender Distribution */}
        <div className="chart-card">
          <h3>Gender Distribution</h3>
          <p className="chart-description">Attendee gender breakdown</p>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={genderData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                label
              >
                {genderData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Nationality Distribution */}
        <div className="chart-card">
          <h3>Nationality Breakdown</h3>
          <p className="chart-description">International reach of our camp</p>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={nationalityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#764ba2" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Registration Timeline */}
        <div className="chart-card">
          <h3>Registration Timeline</h3>
          <p className="chart-description">Track registration pace over time</p>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={analytics.registrationTimeline}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" angle={-45} textAnchor="end" height={80} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="count" stroke="#4facfe" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Assembly Distribution */}
        <div className="chart-card chart-card-wide">
          <h3>Top Assemblies (Churches)</h3>
          <p className="chart-description">Which churches are sending the most attendees</p>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={assemblyData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis type="category" dataKey="name" width={250} />
              <Tooltip content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="custom-tooltip">
                      <p className="label">{payload[0].payload.fullName}</p>
                      <p className="value">Count: {payload[0].value}</p>
                    </div>
                  );
                }
                return null;
              }} />
              <Legend />
              <Bar dataKey="value" fill="#f093fb" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Transportation */}
        <div className="chart-card">
          <h3>Transportation Methods</h3>
          <p className="chart-description">Plan transportation resources</p>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={transportationData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                label
              >
                {transportationData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Allergy Information */}
        <div className="chart-card">
          <h3>Allergy Information</h3>
          <p className="chart-description">Essential for meal planning</p>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={allergyData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                label
              >
                {allergyData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Payment Methods */}
        <div className="chart-card">
          <h3>Payment Methods</h3>
          <p className="chart-description">Track preferred payment options</p>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={paymentData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#43e97b" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Key Insights */}
      <div className="insights-section">
        <h3>💡 Key Insights for Planning</h3>
        <div className="insights-grid">
          <div className="insight-card">
            <h4>Demographics</h4>
            <ul>
              <li>Average age: {analytics.averageAge} years</li>
              <li>Total attendees: {analytics.totalRegistrations}</li>
              <li>Minors requiring chaperone: {analytics.minorsRequiringChaperone}</li>
            </ul>
          </div>

          <div className="insight-card">
            <h4>Churches</h4>
            <ul>
              <li>Participating assemblies: {Object.keys(analytics.assemblyDistribution).length}</li>
              <li>Top church: {Object.entries(analytics.assemblyDistribution).sort((a, b) => b[1] - a[1])[0]?.[0].split('(')[0] || 'N/A'}</li>
              <li>Multi-church event: Yes ✓</li>
            </ul>
          </div>

          <div className="insight-card">
            <h4>Logistics</h4>
            <ul>
              <li>Transportation needed: {Object.values(analytics.transportationStats).reduce((a, b) => a + b, 0)}</li>
              <li>Attendees with allergies: {analytics.allergyStats['Has Allergies'] || 0}</li>
              <li>Nationalities: {Object.keys(analytics.nationalityDistribution).join(', ')}</li>
            </ul>
          </div>

          <div className="insight-card">
            <h4>Payment</h4>
            <ul>
              <li>CashApp: {analytics.paymentOptionStats['CashApp'] || 0}</li>
              <li>Zelle: {analytics.paymentOptionStats['Zelle'] || 0}</li>
              <li>Check: {analytics.paymentOptionStats['Check'] || 0}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
