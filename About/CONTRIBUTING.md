# Contributors Guide

Welcome, and thank you for contributing to our project! To ensure smooth collaboration and maintain code quality, please adhere to the following guidelines:

---

## Tools to Use
- Use **PyCharm Community Edition** or **JetBrains Fleet** as your Integrated Development Environment (IDE) for consistency across contributions; Visual Studio Code would be another option, but I prefer to use the JetBrains IDEs for consistency across contributing.

---

## Coding Standards
1. **Testing**
   - Always test your changes locally before submitting a Pull Request (PR). This helps ensure functionality and avoids introducing bugs to the bot.

2. **Prior Discussions**
   - For large or significant changes, please discuss your plans with the developers before starting. DM, or email the developers.

3. **Command Structure**
   - Use the `@bot.tree.command` structure for implementing Discord bot commands.
   - You also MUST use
   - embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
embed.set_footer(text=f"\n{interaction.user.name} | {datetime.now().strftime('%H:%M:%S')} | COMMAND NAME")
at the end of every command you make.

4. **Python Version**
   - Use **Python 3.12** exclusively. Do not use a lower or higher version to maintain compatibility.
   - We are not planning to upgrade it to Python 3.13 until Python 3.14 comes out.

5. **Comments**
   - Add **#COMMENTs** to your code to make it easy for all contributors to understand. Clear and concise comments are essential for collaboration, so we don't have to ask you every single time. Please use ALL CAPITALS in all comments.

---

## Pull Request Guidelines
- Submit meaningful PRs only. Do not just remove a single space, and think that you've made a change.
- Avoid creating PRs for trivial or unnecessary changes.
- Ensure your PR includes a clear description of what changes were made and why.
- Follow the **coding standards** listed above.

---

We appreciate your contributions! If you have questions, feel free to reach out to the maintainers.
