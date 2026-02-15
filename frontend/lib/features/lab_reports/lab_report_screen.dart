import 'package:flutter/material.dart';
import 'dart:convert';
import '../../core/app_colors.dart';
import '../../core/api_service.dart';

class LabReportScreen extends StatefulWidget {
  const LabReportScreen({super.key});

  @override
  State<LabReportScreen> createState() => _LabReportScreenState();
}

class _LabReportScreenState extends State<LabReportScreen> {
  List<dynamic> _reports = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchReports();
  }

  Future<void> _fetchReports() async {
    try {
      final response = await apiService.get('/lab/reports');
      if (response.statusCode == 200) {
        setState(() {
          _reports = jsonDecode(response.body);
          _isLoading = false;
        });
      }
    } catch (e) {
      setState(() { _isLoading = false; });
    }
  }

  Future<void> _handleUpload() async {
    // In a real mobile app, use FilePicker.
    // For this demonstration, we'll notify the user and simulate a processed result.
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Processing lab report with AI...')),
    );
    // Refresh list after simulation
    _fetchReports();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Lab Reports'),
        elevation: 0,
        backgroundColor: AppColors.white,
        foregroundColor: AppColors.textMain,
      ),
      body: _isLoading 
        ? const Center(child: CircularProgressIndicator())
        : Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              children: [
                _buildUploadCard(),
                const SizedBox(height: 32),
                const Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    'Recent Reports',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                ),
                const SizedBox(height: 16),
                Expanded(
                  child: _reports.isEmpty 
                    ? const Center(child: Text("No reports uploaded yet."))
                    : ListView.builder(
                        itemCount: _reports.length,
                        itemBuilder: (context, index) {
                          final report = _reports[index];
                          return _buildReportItem(
                            report['file_name'],
                            report['date'],
                            report['health_score'],
                            report['summary']
                          );
                        },
                      ),
                ),
              ],
            ),
          ),
    );
  }

  Widget _buildUploadCard() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(32),
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: AppColors.primary.withOpacity(0.2)),
      ),
      child: Column(
        children: [
          Icon(Icons.cloud_upload_outlined, size: 48, color: AppColors.primary),
          const SizedBox(height: 16),
          const Text(
            'Upload Lab Report',
            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
          ),
          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: _handleUpload,
            child: const Text('Select File'),
          ),
        ],
      ),
    );
  }

  Widget _buildReportItem(String title, String date, String status, String summary) {
    bool isWarning = status == 'Attention Needed';
    return InkWell(
      onTap: () {
        showModalBottomSheet(
          context: context,
          builder: (context) => Padding(
            padding: const EdgeInsets.all(24),
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 16),
                  const Text('AI Summary:', style: TextStyle(fontWeight: FontWeight.bold)),
                  Text(summary),
                ],
              ),
            ),
          ),
        );
      },
      child: Container(
        margin: const EdgeInsets.only(bottom: 12),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: AppColors.white,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.grey[100]!),
        ),
        child: Row(
          children: [
            const Icon(Icons.description_outlined, color: Colors.grey),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
                  Text(date, style: TextStyle(color: AppColors.textMuted, fontSize: 12)),
                ],
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(
                color: isWarning ? AppColors.danger.withOpacity(0.1) : AppColors.secondary.withOpacity(0.1),
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(
                status,
                style: TextStyle(
                  color: isWarning ? AppColors.danger : AppColors.secondary,
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
