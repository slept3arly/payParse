"use client";

import { useMemo } from "react";

interface Transaction {
  date: string;
  merchant: string;
  amount: number;
  transaction_type: string;
  category: string;
  status: string;
}

export default function TransactionTable({ transactions }: { transactions: Transaction[] }) {
  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      "Food and Drink": "bg-orange-100 text-orange-700 border-orange-200",
      "Shopping": "bg-purple-100 text-purple-700 border-purple-200",
      "Transfer": "bg-blue-100 text-blue-700 border-blue-200",
      "Automotive": "bg-red-100 text-red-700 border-red-200",
      "Finance": "bg-green-100 text-green-700 border-green-200",
      "Other": "bg-slate-100 text-slate-700 border-slate-200",
    };
    return colors[category] || colors["Other"];
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="border-b border-slate-100 bg-slate-50/30 font-medium text-slate-500 uppercase tracking-tighter">
            <th className="px-6 py-4">Date</th>
            <th className="px-6 py-4">Merchant</th>
            <th className="px-6 py-4">Category</th>
            <th className="px-6 py-4 text-right">Amount</th>
            <th className="px-6 py-4">Status</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {transactions.map((tx, idx) => (
            <tr key={idx} className="group transition-colors hover:bg-slate-50/50">
              <td className="px-6 py-4 whitespace-nowrap text-slate-500">
                {new Date(tx.date).toLocaleDateString()}
              </td>
              <td className="px-6 py-4 font-medium text-slate-900 group-hover:text-blue-600 transition-colors">
                {tx.merchant}
              </td>
              <td className="px-6 py-4">
                <span className={`px-2 py-0.5 rounded-full text-[11px] font-semibold border ${getCategoryColor(tx.category)}`}>
                  {tx.category}
                </span>
              </td>
              <td className="px-6 py-4 text-right font-semibold tabular-nums text-slate-900">
                ₹{tx.amount.toLocaleString()}
              </td>
              <td className="px-6 py-4">
                <span className={`text-xs ${tx.status === 'Completed' ? 'text-green-600' : 'text-amber-600'}`}>
                  {tx.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
