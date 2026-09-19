export type Dataset = {
  id: string;
  name: string;
  type: string;
  size: string;
  rows: number;
  columns: number;
  updatedAt: string;
};

export const datasets: Dataset[] = [
  {
    id: "transactions",
    name: "Transactions",
    type: "CSV",
    size: "2.4 MB",
    rows: 12482,
    columns: 8,
    updatedAt: "2 hours ago",
  },
  {
    id: "students",
    name: "Students",
    type: "XLSX",
    size: "842 KB",
    rows: 1284,
    columns: 12,
    updatedAt: "Yesterday",
  },
  {
    id: "company-db",
    name: "Company Database",
    type: "SQLite",
    size: "18.6 MB",
    rows: 45892,
    columns: 31,
    updatedAt: "3 days ago",
  },
];

export const transactionRows = [
  {
    date: "2026-09-18",
    merchant: "Carrefour",
    category: "Groceries",
    amount: 84.5,
    currency: "MAD",
  },
  {
    date: "2026-09-17",
    merchant: "Uber",
    category: "Transportation",
    amount: 42,
    currency: "MAD",
  },
  {
    date: "2026-09-16",
    merchant: "Netflix",
    category: "Entertainment",
    amount: 95,
    currency: "MAD",
  },
  {
    date: "2026-09-15",
    merchant: "Marjane",
    category: "Groceries",
    amount: 218.3,
    currency: "MAD",
  },
  {
    date: "2026-09-14",
    merchant: "Glovo",
    category: "Food",
    amount: 67,
    currency: "MAD",
  },
];

export const studentColumns = [
  {
    name: "id",
    type: "INTEGER",
    nullable: false,
    key: "PRIMARY KEY",
  },
  {
    name: "first_name",
    type: "VARCHAR",
    nullable: false,
    key: "",
  },
  {
    name: "last_name",
    type: "VARCHAR",
    nullable: false,
    key: "",
  },
  {
    name: "email",
    type: "VARCHAR",
    nullable: false,
    key: "",
  },
  {
    name: "class",
    type: "VARCHAR",
    nullable: true,
    key: "",
  },
  {
    name: "average",
    type: "DECIMAL",
    nullable: true,
    key: "",
  },
];

export const chartData = [
  { month: "Apr", amount: 3200 },
  { month: "May", amount: 4100 },
  { month: "Jun", amount: 3600 },
  { month: "Jul", amount: 5200 },
  { month: "Aug", amount: 4700 },
  { month: "Sep", amount: 3900 },
];