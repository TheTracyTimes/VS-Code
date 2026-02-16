import { Registration, AnalyticsData } from '../types';
import { format } from 'date-fns';

export const calculateAnalytics = (registrations: Registration[]): AnalyticsData => {
  if (registrations.length === 0) {
    return {
      totalRegistrations: 0,
      averageAge: 0,
      ageDistribution: {},
      countryDistribution: {},
      stateProvinceDistribution: {},
      dietaryStats: {},
      transportationStats: {},
      accommodationStats: {},
      interestStats: {},
      financialAidRequests: 0,
      budgetDistribution: {},
      registrationTimeline: [],
      returningVsNew: { returning: 0, new: 0 },
    };
  }

  // Basic stats
  const totalRegistrations = registrations.length;
  const averageAge = registrations.reduce((sum, r) => sum + r.age, 0) / totalRegistrations;

  // Age distribution (grouped by ranges)
  const ageDistribution: { [key: string]: number } = {};
  const ageRanges = ['13-17', '18-24', '25-30', '31-35', '36-40'];
  ageRanges.forEach(range => ageDistribution[range] = 0);

  registrations.forEach(r => {
    if (r.age >= 13 && r.age <= 17) ageDistribution['13-17']++;
    else if (r.age >= 18 && r.age <= 24) ageDistribution['18-24']++;
    else if (r.age >= 25 && r.age <= 30) ageDistribution['25-30']++;
    else if (r.age >= 31 && r.age <= 35) ageDistribution['31-35']++;
    else if (r.age >= 36 && r.age <= 40) ageDistribution['36-40']++;
  });

  // Geographic distribution
  const countryDistribution = countOccurrences(registrations.map(r => r.country));
  const stateProvinceDistribution = countOccurrences(registrations.map(r => r.stateProvince));

  // Dietary restrictions
  const allDietaryRestrictions = registrations.flatMap(r => r.dietaryRestrictions);
  const dietaryStats = countOccurrences(allDietaryRestrictions);

  // Transportation
  const transportationStats = countOccurrences(
    registrations.filter(r => r.transportationNeeded).map(r => r.transportationMethod)
  );

  // Accommodation
  const accommodationStats = countOccurrences(registrations.map(r => r.accommodationType));

  // Program interests
  const allInterests = registrations.flatMap(r => r.interests);
  const interestStats = countOccurrences(allInterests);

  // Financial aid
  const financialAidRequests = registrations.filter(r => r.financialAidNeeded).length;

  // Budget distribution
  const budgetDistribution = countOccurrences(registrations.map(r => r.estimatedBudget));

  // Registration timeline
  const timelineMap = new Map<string, number>();
  registrations.forEach(r => {
    const dateKey = format(new Date(r.timestamp), 'MMM dd, yyyy');
    timelineMap.set(dateKey, (timelineMap.get(dateKey) || 0) + 1);
  });
  const registrationTimeline = Array.from(timelineMap.entries())
    .map(([date, count]) => ({ date, count }))
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

  // Returning vs new attendees
  const returning = registrations.filter(r => r.previouslyAttended).length;
  const newAttendees = totalRegistrations - returning;

  return {
    totalRegistrations,
    averageAge: Math.round(averageAge * 10) / 10,
    ageDistribution,
    countryDistribution,
    stateProvinceDistribution,
    dietaryStats,
    transportationStats,
    accommodationStats,
    interestStats,
    financialAidRequests,
    budgetDistribution,
    registrationTimeline,
    returningVsNew: { returning, new: newAttendees },
  };
};

const countOccurrences = (items: string[]): { [key: string]: number } => {
  return items.reduce((acc, item) => {
    if (item) {
      acc[item] = (acc[item] || 0) + 1;
    }
    return acc;
  }, {} as { [key: string]: number });
};

// Sample data generator for demonstration
export const generateSampleData = (): Registration[] => {
  const countries = ['Canada', 'United States', 'Haiti', 'France', 'Congo'];
  const canadianProvinces = ['Quebec', 'Ontario', 'British Columbia', 'Alberta'];
  const usStates = ['New York', 'California', 'Texas', 'Florida'];
  const cities = ['Montreal', 'Laval', 'Toronto', 'Vancouver', 'New York', 'Miami'];
  const heardAbout = ['Church announcement', 'Friend', 'Social media', 'Website', 'Previous attendee'];
  const interests = ['Worship', 'Bible study', 'Sports', 'Arts & crafts', 'Music', 'Community service', 'Leadership'];
  const dietary = ['None', 'Vegetarian', 'Vegan', 'Gluten-free', 'Halal', 'Nut allergy'];
  const tshirtSizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL'];
  const transportation = ['Personal car', 'Church bus', 'Public transit', 'Carpooling'];
  const accommodation = ['Shared cabin', 'Private room', 'Tent', 'RV'];
  const budgets = ['$0-$100', '$100-$200', '$200-$300', '$300-$500', '$500+'];

  const sampleData: Registration[] = [];

  for (let i = 0; i < 50; i++) {
    const age = Math.floor(Math.random() * 28) + 13; // 13-40
    const country = countries[Math.floor(Math.random() * countries.length)];
    const stateProvince = country === 'Canada'
      ? canadianProvinces[Math.floor(Math.random() * canadianProvinces.length)]
      : country === 'United States'
      ? usStates[Math.floor(Math.random() * usStates.length)]
      : 'N/A';

    const daysAgo = Math.floor(Math.random() * 30);
    const timestamp = new Date();
    timestamp.setDate(timestamp.getDate() - daysAgo);

    sampleData.push({
      id: `reg-${i + 1}`,
      timestamp,
      firstName: `FirstName${i + 1}`,
      lastName: `LastName${i + 1}`,
      age,
      email: `person${i + 1}@example.com`,
      phone: `+1-555-${String(Math.floor(Math.random() * 10000)).padStart(4, '0')}`,
      country,
      stateProvince,
      city: cities[Math.floor(Math.random() * cities.length)],
      previouslyAttended: Math.random() > 0.6,
      timesAttended: Math.random() > 0.6 ? Math.floor(Math.random() * 5) + 1 : 0,
      heardAboutCamp: heardAbout[Math.floor(Math.random() * heardAbout.length)],
      interests: interests.filter(() => Math.random() > 0.5).slice(0, 3),
      dietaryRestrictions: Math.random() > 0.7 ? [dietary[Math.floor(Math.random() * dietary.length)]] : ['None'],
      tShirtSize: tshirtSizes[Math.floor(Math.random() * tshirtSizes.length)],
      transportationNeeded: Math.random() > 0.3,
      transportationMethod: transportation[Math.floor(Math.random() * transportation.length)],
      accommodationType: accommodation[Math.floor(Math.random() * accommodation.length)],
      financialAidNeeded: Math.random() > 0.7,
      estimatedBudget: budgets[Math.floor(Math.random() * budgets.length)],
      emergencyContactName: `Contact${i + 1}`,
      emergencyContactPhone: `+1-555-${String(Math.floor(Math.random() * 10000)).padStart(4, '0')}`,
      emergencyContactRelation: ['Parent', 'Spouse', 'Sibling', 'Friend'][Math.floor(Math.random() * 4)],
      specialNeeds: '',
      comments: '',
    });
  }

  return sampleData;
};
