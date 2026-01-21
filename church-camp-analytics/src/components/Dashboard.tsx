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

  const countryData = Object.entries(analytics.countryDistribution)
    .map(([country, count]) => ({ country, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10);

  const stateData = Object.entries(analytics.stateProvinceDistribution)
    .map(([state, count]) => ({ state, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10);

  const dietaryData = Object.entries(analytics.dietaryStats)
    .map(([name, value]) => ({ name, value }))
    .filter(item => item.name !== 'None');

  const transportationData = Object.entries(analytics.transportationStats).map(([name, value]) => ({
    name,
    value,
  }));

  const accommodationData = Object.entries(analytics.accommodationStats).map(([name, value]) => ({
    name,
    value,
  }));

  const interestData = Object.entries(analytics.interestStats)
    .map(([name, value]) => ({ name, value }))
    .sort((a, b) => b.value - a.value);

  const budgetData = Object.entries(analytics.budgetDistribution).map(([name, value]) => ({
    name,
    value,
  }));

  const attendeeTypeData = [
    { name: 'Returning', value: analytics.returningVsNew.returning },
    { name: 'New', value: analytics.returningVsNew.new },
  ];

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Camp Registration Analytics Dashboard</h2>
        <p className="dashboard-subtitle">Real-time insights for planning and cost analysis</p>
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
          <div className="metric-icon">💰</div>
          <div className="metric-content">
            <h3>Financial Aid Requests</h3>
            <p className="metric-value">{analytics.financialAidRequests}</p>
            <p className="metric-subtitle">
              {analytics.totalRegistrations > 0
                ? `${Math.round((analytics.financialAidRequests / analytics.totalRegistrations) * 100)}%`
                : '0%'}{' '}
              of total
            </p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">🔄</div>
          <div className="metric-content">
            <h3>Returning Attendees</h3>
            <p className="metric-value">{analytics.returningVsNew.returning}</p>
            <p className="metric-subtitle">
              {analytics.totalRegistrations > 0
                ? `${Math.round((analytics.returningVsNew.returning / analytics.totalRegistrations) * 100)}%`
                : '0%'}{' '}
              retention
            </p>
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="charts-grid">
        {/* Age Distribution */}
        <div className="chart-card">
          <h3>Age Distribution</h3>
          <p className="chart-description">Understanding our demographic spread helps plan age-appropriate activities</p>
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

        {/* Geographic Distribution - Countries */}
        <div className="chart-card">
          <h3>Registrations by Country</h3>
          <p className="chart-description">International distribution helps plan logistics and transportation</p>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={countryData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis type="category" dataKey="country" width={100} />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#764ba2" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* States/Provinces */}
        <div className="chart-card">
          <h3>Top States/Provinces</h3>
          <p className="chart-description">Regional distribution for organizing carpools and local meetups</p>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={stateData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="state" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#f093fb" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Registration Timeline */}
        <div className="chart-card">
          <h3>Registration Timeline</h3>
          <p className="chart-description">Track registration pace to optimize marketing efforts</p>
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

        {/* Dietary Restrictions */}
        <div className="chart-card">
          <h3>Dietary Restrictions</h3>
          <p className="chart-description">Essential for meal planning and catering budget</p>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={dietaryData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                label
              >
                {dietaryData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Transportation Needs */}
        <div className="chart-card">
          <h3>Transportation Methods</h3>
          <p className="chart-description">Plan transportation resources and associated costs</p>
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

        {/* Accommodation Preferences */}
        <div className="chart-card">
          <h3>Accommodation Preferences</h3>
          <p className="chart-description">Allocate facilities and estimate accommodation costs</p>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={accommodationData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#43e97b" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Program Interests */}
        <div className="chart-card">
          <h3>Program Interest Levels</h3>
          <p className="chart-description">Allocate staff and resources based on popularity</p>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={interestData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis type="category" dataKey="name" width={120} />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#fa709a" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Budget Distribution */}
        <div className="chart-card">
          <h3>Budget Distribution</h3>
          <p className="chart-description">Understand attendee budgets for pricing strategy</p>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={budgetData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#fee140" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* New vs Returning */}
        <div className="chart-card">
          <h3>New vs Returning Attendees</h3>
          <p className="chart-description">Measure camp retention and growth</p>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={attendeeTypeData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                label
              >
                {attendeeTypeData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Cost Analysis Insights */}
      <div className="insights-section">
        <h3>💡 Key Insights for Planning</h3>
        <div className="insights-grid">
          <div className="insight-card">
            <h4>Demographics</h4>
            <ul>
              <li>Average age: {analytics.averageAge} years</li>
              <li>Total attendees: {analytics.totalRegistrations}</li>
              <li>Geographic diversity: {Object.keys(analytics.countryDistribution).length} countries</li>
            </ul>
          </div>

          <div className="insight-card">
            <h4>Financial Planning</h4>
            <ul>
              <li>Financial aid requests: {analytics.financialAidRequests}</li>
              <li>Most common budget: {Object.entries(analytics.budgetDistribution).sort((a, b) => b[1] - a[1])[0]?.[0] || 'N/A'}</li>
              <li>Aid percentage: {analytics.totalRegistrations > 0 ? Math.round((analytics.financialAidRequests / analytics.totalRegistrations) * 100) : 0}%</li>
            </ul>
          </div>

          <div className="insight-card">
            <h4>Logistics</h4>
            <ul>
              <li>Transportation needed: {Object.values(analytics.transportationStats).reduce((a, b) => a + b, 0)}</li>
              <li>Special dietary needs: {Object.entries(analytics.dietaryStats).filter(([key]) => key !== 'None').reduce((sum, [, val]) => sum + val, 0)}</li>
              <li>Most popular activity: {Object.entries(analytics.interestStats).sort((a, b) => b[1] - a[1])[0]?.[0] || 'N/A'}</li>
            </ul>
          </div>

          <div className="insight-card">
            <h4>Retention</h4>
            <ul>
              <li>Returning attendees: {analytics.returningVsNew.returning}</li>
              <li>New attendees: {analytics.returningVsNew.new}</li>
              <li>Retention rate: {analytics.totalRegistrations > 0 ? Math.round((analytics.returningVsNew.returning / analytics.totalRegistrations) * 100) : 0}%</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
