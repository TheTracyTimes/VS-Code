import type { Registration, AnalyticsData } from '../types';
import { format } from 'date-fns';

export const calculateAnalytics = (registrations: Registration[]): AnalyticsData => {
  if (registrations.length === 0) {
    return {
      totalRegistrations: 0,
      averageAge: 0,
      ageDistribution: {},
      genderDistribution: {},
      nationalityDistribution: {},
      assemblyDistribution: {},
      transportationStats: {},
      allergyStats: {},
      paymentOptionStats: {},
      registrationTimeline: [],
      minorsRequiringChaperone: 0,
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

  // Gender distribution
  const genderDistribution = countOccurrences(registrations.map(r => r.gender));

  // Nationality distribution
  const nationalityDistribution = countOccurrences(registrations.map(r => r.nationality));

  // Assembly distribution
  const assemblyDistribution = countOccurrences(registrations.map(r => r.assembly));

  // Transportation
  const transportationStats = countOccurrences(registrations.map(r => r.transportation).filter(t => t));

  // Allergies (count those with allergies)
  const allergyStats = countOccurrences(
    registrations.filter(r => r.allergies && r.allergies.toLowerCase() !== 'none' && r.allergies.trim() !== '')
      .map(() => 'Has Allergies')
  );
  const noAllergies = registrations.filter(
    r => !r.allergies || r.allergies.toLowerCase() === 'none' || r.allergies.trim() === ''
  ).length;
  if (noAllergies > 0) {
    allergyStats['No Allergies'] = noAllergies;
  }

  // Payment options
  const paymentOptionStats = countOccurrences(registrations.map(r => r.paymentOption));

  // Registration timeline
  const timelineMap = new Map<string, number>();
  registrations.forEach(r => {
    const dateKey = format(new Date(r.timestamp), 'MMM dd, yyyy');
    timelineMap.set(dateKey, (timelineMap.get(dateKey) || 0) + 1);
  });
  const registrationTimeline = Array.from(timelineMap.entries())
    .map(([date, count]) => ({ date, count }))
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

  // Minors requiring chaperone
  const minorsRequiringChaperone = registrations.filter(r => r.age < 18).length;

  return {
    totalRegistrations,
    averageAge: Math.round(averageAge * 10) / 10,
    ageDistribution,
    genderDistribution,
    nationalityDistribution,
    assemblyDistribution,
    transportationStats,
    allergyStats,
    paymentOptionStats,
    registrationTimeline,
    minorsRequiringChaperone,
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
  const genders = ['Female', 'Male'];
  const nationalities = ['Canadian', 'American', 'French'];
  const assemblies = [
    'Assemblée Évangélique de Laval (Pastor Exavier Noel & Pastor Rosage Beauzil)',
    'Assemblée Évangélique de Montreal (Pastor David Paul)',
    'Tabernacle Evangelique Mahanaim (Pastor Gesner Dorzin)',
    'Gospel Assembly of the Kingdom of Peace (Pastor Ancelot Joseph)',
    'Christian Family Gospel Assembly (Pastor Kennedy Demosthenes)',
    'Eglise de la Nouvelle Alliance (Pastor Vitalerme Dorestant)',
    'Other',
  ];
  const transportation = ['Personal car', 'Church bus', 'Carpooling', 'Public transit', 'Need ride'];
  const paymentOptions = ['CashApp', 'Zelle', 'Check'];
  const allergies = ['None', 'Peanuts', 'Lactose', 'Shellfish', 'Gluten'];

  const sampleData: Registration[] = [];

  for (let i = 0; i < 50; i++) {
    const age = Math.floor(Math.random() * 28) + 13; // 13-40
    const gender = genders[Math.floor(Math.random() * genders.length)];
    const nationality = nationalities[Math.floor(Math.random() * nationalities.length)];
    const assembly = assemblies[Math.floor(Math.random() * assemblies.length)];

    const daysAgo = Math.floor(Math.random() * 30);
    const timestamp = new Date();
    timestamp.setDate(timestamp.getDate() - daysAgo);

    sampleData.push({
      id: `reg-${i + 1}`,
      timestamp,
      firstName: `FirstName${i + 1}`,
      lastName: `LastName${i + 1}`,
      gender,
      age,
      chaperoneName: age < 18 ? `Chaperone${i + 1}` : '',
      phone: `+1-555-${String(Math.floor(Math.random() * 10000)).padStart(4, '0')}`,
      email: `person${i + 1}@example.com`,
      nationality,
      assembly,
      transportation: transportation[Math.floor(Math.random() * transportation.length)],
      allergies: allergies[Math.floor(Math.random() * allergies.length)],
      emergencyContactName: `Contact${i + 1}`,
      emergencyContactPhone: `+1-555-${String(Math.floor(Math.random() * 10000)).padStart(4, '0')}`,
      comments: '',
      concerns: '',
      questions: '',
      paymentOption: paymentOptions[Math.floor(Math.random() * paymentOptions.length)],
    });
  }

  return sampleData;
};
