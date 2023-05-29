import logging
from telegram import Update
from telegram.ext import (Updater, CommandHandler, ConversationHandler, MessageHandler, Filters)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Conversation state
COMPLAINT_DESCRIPTION = 1

# Start command handler
def start(update: Update, context):
    user = update.message.from_user
    update.message.reply_text(
        f"Hello {user.first_name}! Welcome to the ticket bot. "
        "Please provide a description of your complaint."
    )
    return COMPLAINT_DESCRIPTION

# Complaint description handler
def complaint_description(update: Update, context):
    user = update.message.from_user
    complaint_description_text = update.message.text
    context.user_data['complaint_description'] = complaint_description_text

    # Generate the ticket ID
    ticket_id = f"#{len(context.user_data['complaint_description']):04}"

    # Process the complaint here
    # You can save the complaint description, contact information, username/user ID, and ticket ID in a database or perform any necessary actions

    # Get the username or user ID
    username = user.username or str(user.id)

    # Forward the message to the specific group using its group ID
    group_id = "YOUR_GROUP_ID"
    context.bot.send_message(
        chat_id=group_id,
        text=f"New Ticket:\n\nTicket ID: {ticket_id}\n\nUsername/User ID: @{username}\n\nComplaint Description: {context.user_data['complaint_description']}"
    )

    update.message.reply_text(
        f"Thank you for submitting the complaint. Your ticket ID is {ticket_id}. We will get back to you soon."
    )
    return ConversationHandler.END

# Cancel command handler
def cancel(update: Update, context):
    user = update.message.from_user
    update.message.reply_text(
        "Complaint submission canceled."
    )
    return ConversationHandler.END

# Main function
def main():
    # Create the Updater and dispatcher
    updater = Updater("YOUR_API_KEY", use_context=True)
    dp = updater.dispatcher

    # Create the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            COMPLAINT_DESCRIPTION: [MessageHandler(Filters.text, complaint_description)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Add the conversation handler to the dispatcher
    dp.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

