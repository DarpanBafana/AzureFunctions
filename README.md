# Introduction 
TODO: Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project. 

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references

# Build and Test
TODO: Describe and show how to build your code and run the tests. 

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)

# Important Guidelines
1. Won't allow duplicate addresses in To,Cc, Bcc - unique email address in the personalizations array
2. These 7 fields are mandatory either you pass null or blank array/string
{
	"sender_address" : "sender@vizientinc.com",
	"email_subject" : "Enter Subject",
	"recipient_address" : "receiver@vizientinc.com",
	"email_content" : "Enter Content",
	"cc_recipient_address" : null,
	"html_content": null,
	"with_attachment": null
}
3. Plain text/Html both supported. But when you send Html test and plain text both. It will pick html content.
