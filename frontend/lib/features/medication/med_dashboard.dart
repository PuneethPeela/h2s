import 'package:flutter/material.dart';
import '../../core/app_colors.dart';

class MedicationDashboard extends StatelessWidget {
  const MedicationDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Medications'),
        elevation: 0,
        backgroundColor: AppColors.white,
        foregroundColor: AppColors.textMain,
      ),
      body: ListView(
        padding: const EdgeInsets.all(24),
        children: [
          _buildSummaryCard(),
          const SizedBox(height: 32),
          const Text(
            'Today\'s Schedule',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 16),
          _buildMedItem('Amoxicillin', '500mg - 1 capsule', '08:00 AM', true),
          _buildMedItem('Vitamin D3', '2000 IU', '12:30 PM', false),
          _buildMedItem('Metformin', '850mg', '07:00 PM', false),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        backgroundColor: AppColors.primary,
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildSummaryCard() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [AppColors.primary, AppColors.primaryDark],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: AppColors.primary.withOpacity(0.3),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Adherence Score',
            style: TextStyle(color: Colors.white70, fontSize: 14),
          ),
          const SizedBox(height: 4),
          const Text(
            '92%',
            style: TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 16),
          const Text(
            'Great job! You\'ve taken 4/5 doses this week.',
            style: TextStyle(color: Colors.white, fontSize: 14),
          ),
        ],
      ),
    );
  }

  Widget _buildMedItem(String name, String dose, String time, bool isTaken) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.grey[100]!),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: isTaken ? AppColors.secondary.withOpacity(0.1) : AppColors.primary.withOpacity(0.1),
              shape: BoxShape.circle,
            ),
            child: Icon(
              isTaken ? Icons.check : Icons.medication_outlined,
              color: isTaken ? AppColors.secondary : AppColors.primary,
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                Text('$dose • $time', style: TextStyle(color: AppColors.textMuted, fontSize: 13)),
              ],
            ),
          ),
          if (!isTaken)
            TextButton(
              onPressed: () {},
              child: const Text('Mark Taken'),
            ),
        ],
      ),
    );
  }
}
