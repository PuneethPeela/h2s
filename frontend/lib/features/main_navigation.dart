import 'package:flutter/material.dart';
import 'package:lucide_icons/lucide_icons.dart';
import '../core/app_colors.dart';
import 'chat/chat_screen.dart';
import 'medication/med_dashboard.dart';
import 'lab_reports/lab_report_screen.dart';
import 'care_navigation/care_navigation_screen.dart';

class MainNavigation extends StatefulWidget {
  const MainNavigation({super.key});

  @override
  State<MainNavigation> createState() => _MainNavigationState();
}

class _MainNavigationState extends State<MainNavigation> {
  int _selectedIndex = 0;

  final List<Widget> _screens = [
    const ChatScreen(),
    const MedicationDashboard(),
    const LabReportScreen(),
    const CareNavigationScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _selectedIndex,
        children: _screens,
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) => setState(() => _selectedIndex = index),
        type: BottomNavigationBarType.fixed,
        selectedItemColor: AppColors.primary,
        unselectedItemColor: AppColors.textMuted,
        showUnselectedLabels: true,
        items: const [
          BottomNavigationBarItem(icon: Icon(LucideIcons.messageSquare), label: 'AI Chat'),
          BottomNavigationBarItem(icon: Icon(LucideIcons.pill), label: 'Meds'),
          BottomNavigationBarItem(icon: Icon(LucideIcons.fileText), label: 'Reports'),
          BottomNavigationBarItem(icon: Icon(LucideIcons.map), label: 'Care'),
        ],
      ),
    );
  }
}
