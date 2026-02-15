import 'package:flutter/material.dart';
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:uuid/uuid.dart';
import '../../core/app_colors.dart';
import '../symptom_checker/symptom_screen.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final List<types.Message> _messages = [];
  final _user = const types.User(id: 'user-id');
  final _ai = const types.User(id: 'ai-id', firstName: 'Health AI');
  
  @override
  void initState() {
    super.initState();
    _addMessage("Hello! I'm your AI health assistant. How can I help you today?", isUser: false);
  }

  void _addMessage(String text, {required bool isUser}) {
    final message = types.TextMessage(
      author: isUser ? _user : _ai,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: const Uuid().v4(),
      text: text,
    );
    setState(() {
      _messages.insert(0, message);
    });
  }

  void _handleSendPressed(types.PartialText message) {
    _addMessage(message.text, isUser: true);
    
    // Simulate AI response for demo
    Future.delayed(const Duration(seconds: 1), () {
      _addMessage("I understand. It sounds like you're asking about ${message.text}. Let me check our medical database...", isUser: false);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Health Assistant'),
        backgroundColor: AppColors.white,
        foregroundColor: AppColors.textMain,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.medical_services_outlined),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const SymptomScreen()),
              );
            },
          ),
        ],
      ),
      body: Chat(
        messages: _messages,
        onSendPressed: _handleSendPressed,
        user: _user,
        theme: DefaultChatTheme(
          primaryColor: AppColors.primary,
          secondaryColor: Colors.grey[200]!,
          inputBackgroundColor: AppColors.white,
          inputTextColor: AppColors.textMain,
        ),
      ),
    );
  }
}
