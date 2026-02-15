import 'package:flutter/material.dart';
import 'dart:convert';
import '../../core/app_colors.dart';
import '../../core/api_service.dart';

class CareNavigationScreen extends StatefulWidget {
  const CareNavigationScreen({super.key});

  @override
  State<CareNavigationScreen> createState() => _CareNavigationScreenState();
}

class _CareNavigationScreenState extends State<CareNavigationScreen> {
  List<dynamic> _appointments = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchAppointments();
  }

  Future<void> _fetchAppointments() async {
    try {
      final response = await apiService.get('/appointments/');
      if (response.statusCode == 200) {
        setState(() {
          _appointments = jsonDecode(response.body);
          _isLoading = false;
        });
      }
    } catch (e) {
       setState(() { _isLoading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Care Navigation'),
        elevation: 0,
        backgroundColor: AppColors.white,
        foregroundColor: AppColors.textMain,
      ),
      body: _isLoading 
        ? const Center(child: CircularProgressIndicator())
        : ListView(
            padding: const EdgeInsets.all(24),
            children: [
              const Text(
                'Your Care Plan',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 24),
              if (_appointments.isEmpty)
                _buildEmptyState()
              else
                ..._appointments.map((a) => _buildAppointmentCard(
                  a['doctor_name'],
                  a['specialty'] ?? 'Specialist',
                  a['appointment_time'],
                  a['location'] ?? 'Medical Center',
                )).toList(),
              const SizedBox(height: 32),
              const Text(
                'Recommended Next Steps',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 16),
              _buildActionItem(
                Icons.calendar_today_outlined,
                'Schedule Blood Work',
                'Based on your last lab report analysis.',
              ),
              _buildActionItem(
                Icons.assignment_outlined,
                'Complete Health Questionnaire',
                'Update your profile for better AI insights.',
              ),
            ],
          ),
    );
  }

  Widget _buildEmptyState() {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.grey[50],
        borderRadius: BorderRadius.circular(20),
      ),
      child: const Column(
        children: [
          Icon(Icons.event_available, size: 48, color: Colors.grey),
          SizedBox(height: 16),
          Text("No upcoming appointments."),
          SizedBox(height: 8),
          Text("Keep your care plan updated by scheduling your next visit."),
        ],
      ),
    );
  }

  Widget _buildAppointmentCard(String name, String specialty, String time, String location) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.grey[200]!),
        boxShadow: [
          BoxShadow(color: Colors.black.withOpacity(0.02), blurRadius: 10, offset: const Offset(0, 4)),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              CircleAvatar(
                backgroundColor: AppColors.primary.withOpacity(0.1),
                child: const Icon(Icons.person, color: AppColors.primary),
              ),
              const SizedBox(width: 12),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                  Text(specialty, style: TextStyle(color: AppColors.textMuted, fontSize: 13)),
                ],
              ),
              const Spacer(),
              const Icon(Icons.more_vert),
            ],
          ),
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 16),
            child: Divider(),
          ),
          Row(
            children: [
              const Icon(Icons.access_time, size: 16, color: AppColors.textMuted),
              const SizedBox(width: 8),
              Text(time, style: const TextStyle(fontSize: 13)),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              const Icon(Icons.location_on_outlined, size: 16, color: AppColors.textMuted),
              const SizedBox(width: 8),
              Text(location, style: const TextStyle(fontSize: 13)),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildActionItem(IconData icon, String title, String subtitle) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.grey[50],
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        children: [
          Icon(icon, color: AppColors.primary),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
                Text(subtitle, style: TextStyle(color: AppColors.textMuted, fontSize: 12)),
              ],
            ),
          ),
          const Icon(Icons.chevron_right, color: Colors.grey),
        ],
      ),
    );
  }
}
