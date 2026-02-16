export interface Registration {
  id: string;
  timestamp: Date;

  // Personal Information
  firstName: string;
  lastName: string;
  age: number;
  email: string;
  phone: string;

  // Geographic Information
  country: string;
  stateProvince: string;
  city: string;

  // Camp Details
  previouslyAttended: boolean;
  timesAttended: number;
  heardAboutCamp: string;

  // Program Interests (multiple selection)
  interests: string[];

  // Logistics & Cost Factors
  dietaryRestrictions: string[];
  tShirtSize: string;
  transportationNeeded: boolean;
  transportationMethod: string;
  accommodationType: string;
  financialAidNeeded: boolean;
  estimatedBudget: string;

  // Emergency Contact
  emergencyContactName: string;
  emergencyContactPhone: string;
  emergencyContactRelation: string;

  // Additional Information
  specialNeeds: string;
  comments: string;
}

export interface AnalyticsData {
  totalRegistrations: number;
  averageAge: number;
  ageDistribution: { [key: string]: number };
  countryDistribution: { [key: string]: number };
  stateProvinceDistribution: { [key: string]: number };
  dietaryStats: { [key: string]: number };
  transportationStats: { [key: string]: number };
  accommodationStats: { [key: string]: number };
  interestStats: { [key: string]: number };
  financialAidRequests: number;
  budgetDistribution: { [key: string]: number };
  registrationTimeline: { date: string; count: number }[];
  returningVsNew: { returning: number; new: number };
}
