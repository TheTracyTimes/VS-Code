# ⛺ Church Camp Analytics Platform

An interactive, educational data analytics and visualization platform designed for church camp registration. This application demonstrates real-time data visualization, interactive forms, and comprehensive analytics for learning data analytics and UI/UX design principles.

## 🎯 Purpose

This platform serves multiple objectives:

1. **Educational Tool**: Teaches data analytics concepts through real-world camp registration data
2. **UI/UX Learning**: Demonstrates modern web design principles and user experience best practices
3. **Camp Planning**: Provides insights for future camp planning and cost analysis
4. **Data Visualization**: Shows how to transform raw data into meaningful visualizations

## ✨ Features

### 📝 Comprehensive Registration Form
- Personal information collection (name, age, contact details)
- Geographic data (country, state/province, city)
- Camp experience tracking (returning vs. new attendees)
- Program interests selection
- Dietary restrictions and special needs
- Transportation and accommodation preferences
- Financial aid tracking and budget information
- Emergency contact information

### 📊 Real-Time Analytics Dashboard
- **Key Metrics Cards**: Total registrations, average age, financial aid requests, retention rate
- **Age Distribution Chart**: Visualizes age ranges (13-40) with bar charts
- **Geographic Analysis**:
  - Country distribution
  - State/Province breakdown
- **Registration Timeline**: Track registration pace over time
- **Dietary Restrictions**: Pie chart for meal planning
- **Transportation Analysis**: Understand logistics needs
- **Accommodation Preferences**: Plan facility allocation
- **Program Interests**: Identify popular activities
- **Budget Distribution**: Pricing strategy insights
- **Retention Metrics**: New vs. returning attendees

### 💾 Data Management
- **Local Storage**: Automatic data persistence
- **Sample Data**: Pre-loaded demo data for exploration
- **Export Functionality**:
  - JSON export for developers
  - CSV export for spreadsheet analysis
- **Data Clearing**: Reset functionality with confirmation

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm

### Installation

1. Navigate to the project directory:
```bash
cd church-camp-analytics
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser to `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The build output will be in the `dist` folder.

## 🛠️ Technology Stack

- **Frontend Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Charting Library**: Recharts
- **Date Utilities**: date-fns
- **Styling**: CSS3 with modern features
- **Data Persistence**: LocalStorage API

## 📚 Learning Opportunities

This project demonstrates:

1. **Data Analytics Concepts**:
   - Data aggregation and transformation
   - Statistical calculations (averages, distributions)
   - Time-series analysis
   - Categorical data visualization
   - Demographic analysis

2. **UI/UX Design Principles**:
   - Form design best practices
   - Progressive disclosure
   - Visual hierarchy
   - Color theory and gradients
   - Responsive design
   - Interactive feedback
   - Loading states and animations

3. **Frontend Development**:
   - React hooks (useState, useEffect)
   - Component composition
   - TypeScript type safety
   - Data flow management
   - Event handling
   - Local storage integration

## 📊 Data Analytics Insights

The platform provides insights for:

### Camp Planning
- Understand attendee demographics
- Plan age-appropriate activities
- Allocate resources based on interests

### Cost Analysis
- Financial aid demand assessment
- Budget distribution understanding
- Transportation cost estimation
- Accommodation resource planning
- Catering requirements (dietary needs)

### Marketing & Retention
- Track how people hear about the camp
- Measure retention rates
- Identify growth trends
- Geographic reach analysis

### Logistics
- Transportation coordination
- Accommodation allocation
- Special needs planning
- Resource optimization

## 🎨 Design Features

- **Modern Gradient Design**: Purple-blue gradient theme
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Interactive Charts**: Hover effects and tooltips
- **Smooth Animations**: Transitions and loading states
- **Accessible Forms**: Clear labels and validation
- **Visual Feedback**: Success notifications and button states

## 🎓 Target Audience

- **Age Range**: 13-40 (youth to young adults)
- **Context**: Church camp attendees
- **Use Case**: Registration and planning for Assemblée Évangélique de Laval

## 📁 Project Structure

```
church-camp-analytics/
├── src/
│   ├── components/
│   │   ├── RegistrationForm.tsx    # Comprehensive registration form
│   │   ├── RegistrationForm.css    # Form styling
│   │   ├── Dashboard.tsx            # Analytics dashboard
│   │   └── Dashboard.css            # Dashboard styling
│   ├── utils/
│   │   └── analytics.ts             # Data processing and sample data
│   ├── types.ts                     # TypeScript type definitions
│   ├── App.tsx                      # Main application component
│   ├── App.css                      # Application styling
│   ├── index.css                    # Global styles
│   └── main.tsx                     # Application entry point
├── public/                          # Static assets
├── package.json                     # Dependencies and scripts
├── tsconfig.json                    # TypeScript configuration
├── vite.config.ts                   # Vite configuration
└── README.md                        # This file
```

## 🔄 Data Flow

1. User fills out registration form
2. Form data is validated
3. Registration is added to state
4. Data is persisted to localStorage
5. Analytics are calculated in real-time
6. Dashboard visualizations update automatically
7. User can export data in JSON or CSV format

## 🌟 Future Enhancements

Potential additions for extended learning:
- Backend integration with a REST API
- Database storage (MongoDB, PostgreSQL)
- User authentication and roles
- Email notifications
- Payment processing integration
- PDF report generation
- Advanced filtering and search
- Data comparison across years
- Predictive analytics

## 👥 Educational Value

This project is ideal for:
- Learning modern web development
- Understanding data visualization
- Practicing TypeScript
- Exploring React patterns
- Studying form design
- Analyzing user experience
- Building real-world applications

## 📞 Support

For questions or issues, please refer to the church's contact information:
- YouTube: [@assembleeevangeliquedelaval](https://www.youtube.com/@assembleeevangeliquedelaval)
- Instagram: [@assemblee.evangelique.de.laval](https://www.instagram.com/assemblee.evangelique.de.laval)

## 📄 License

This project is for educational purposes and church camp management.

---

Built with ❤️ for learning data analytics and UI/UX design | Assemblée Évangélique de Laval
