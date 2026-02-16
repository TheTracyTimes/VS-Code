export interface Registration {
  id: string;
  timestamp: Date;

  // Personal Information
  firstName: string;
  lastName: string;
  gender: string;
  age: number;
  chaperoneName: string; // Required if under 18
  phone: string;
  email: string;
  nationality: string;

  // Church Information
  assembly: string;

  // Transportation & Logistics
  transportation: string;
  allergies: string;

  // Emergency Contact
  emergencyContactName: string;
  emergencyContactPhone: string;

  // Additional Information
  comments: string;
  concerns: string;
  questions: string;

  // Payment
  paymentOption: string;
}

export interface AnalyticsData {
  totalRegistrations: number;
  averageAge: number;
  ageDistribution: { [key: string]: number };
  genderDistribution: { [key: string]: number };
  nationalityDistribution: { [key: string]: number };
  assemblyDistribution: { [key: string]: number };
  transportationStats: { [key: string]: number };
  allergyStats: { [key: string]: number };
  paymentOptionStats: { [key: string]: number };
  registrationTimeline: { date: string; count: number }[];
  minorsRequiringChaperone: number;
}
