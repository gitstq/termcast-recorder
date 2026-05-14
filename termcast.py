#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 TermCast - Lightweight Terminal Session Recording & Smart Replay Engine
轻量级终端会话录制与智能回放引擎

A zero-dependency Python CLI tool for recording, analyzing, and replaying
terminal sessions with intelligent command categorization and multi-format export.

Author: TermCast Team
License: MIT
Version: 1.0.0
"""

import sys
import os
import time
import json
import argparse
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum


class CommandCategory(Enum):
    """Command categories for intelligent classification"""
    GIT = "git"
    DOCKER = "docker"
    FILE_OP = "file_op"
    SYSTEM = "system"
    NETWORK = "network"
    BUILD = "build"
    TEST = "test"
    DEPLOY = "deploy"
    DATABASE = "database"
    EDIT = "edit"
    OTHER = "other"


@dataclass
class CommandEntry:
    """Represents a single command entry in the session"""
    timestamp: float
    command: str
    output: str = ""
    exit_code: int = 0
    duration: float = 0.0
    category: str = CommandCategory.OTHER.value
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SessionMetadata:
    """Session metadata"""
    session_id: str
    created_at: str
    shell: str
    user: str
    hostname: str
    cwd: str
    term_size: Tuple[int, int]
    total_commands: int = 0
    duration_seconds: float = 0.0


class CommandClassifier:
    """Intelligent command classifier"""

    PATTERNS = {
        CommandCategory.GIT: [
            r'^git\s+',
            r'^gh\s+',
        ],
        CommandCategory.DOCKER: [
            r'^docker\s+',
            r'^docker-compose\s+',
            r'^podman\s+',
        ],
        CommandCategory.FILE_OP: [
            r'^ls\s+', r'^ll\s*', r'^la\s*',
            r'^cd\s+', r'^pwd\s*',
            r'^cp\s+', r'^mv\s+', r'^rm\s+',
            r'^mkdir\s+', r'^rmdir\s+',
            r'^touch\s+', r'^cat\s+',
            r'^find\s+', r'^grep\s+',
            r'^tar\s+', r'^zip\s+', r'^unzip\s+',
        ],
        CommandCategory.SYSTEM: [
            r'^ps\s*', r'^top\s*', r'^htop\s*',
            r'^df\s*', r'^du\s+',
            r'^free\s*', r'^uname\s*',
            r'^sudo\s+', r'^su\s+',
            r'^chmod\s+', r'^chown\s+',
            r'^systemctl\s+', r'^service\s+',
        ],
        CommandCategory.NETWORK: [
            r'^ping\s+', r'^curl\s+', r'^wget\s+',
            r'^ssh\s+', r'^scp\s+',
            r'^netstat\s*', r'^ss\s*',
            r'^ifconfig\s*', r'^ip\s+',
            r'^nc\s+', r'^telnet\s+',
        ],
        CommandCategory.BUILD: [
            r'^make\s*', r'^cmake\s+',
            r'^npm\s+', r'^yarn\s+', r'^pnpm\s+',
            r'^pip\s+', r'^poetry\s+',
            r'^cargo\s+', r'^go\s+build',
            r'^gcc\s+', r'^g\+\+\s+',
            r'^javac\s+', r'^gradle\s+', r'^mvn\s+',
        ],
        CommandCategory.TEST: [
            r'^pytest\s*', r'^python\s+-m\s+pytest',
            r'^npm\s+test', r'^yarn\s+test',
            r'^cargo\s+test',
            r'^go\s+test',
            r'^jest\s*', r'^mocha\s*',
        ],
        CommandCategory.DEPLOY: [
            r'^kubectl\s+', r'^helm\s+',
            r'^terraform\s+', r'^ansible\s+',
            r'^serverless\s+', r'^sls\s+',
            r'^vercel\s+', r'^netlify\s+',
            r'^aws\s+', r'^gcloud\s+', r'^az\s+',
        ],
        CommandCategory.DATABASE: [
            r'^mysql\s+', r'^psql\s+',
            r'^mongo\s+', r'^redis\s*',
            r'^sqlite3?\s+',
        ],
        CommandCategory.EDIT: [
            r'^vim?\s+', r'^nvim\s+',
            r'^nano\s+', r'^emacs\s+',
            r'^code\s+', r'^subl\s+',
        ],
    }

    @classmethod
    def classify(cls, command: str) -> CommandCategory:
        """Classify a command into a category"""
        command = command.strip().lower()
        for category, patterns in cls.PATTERNS.items():
            for pattern in patterns:
                if re.match(pattern, command):
                    return category
        return CommandCategory.OTHER

    @classmethod
    def get_description(cls, category: CommandCategory) -> str:
        """Get human-readable description for category"""
        descriptions = {
            CommandCategory.GIT: "🌿 Version Control",
            CommandCategory.DOCKER: "🐳 Container Operations",
            CommandCategory.FILE_OP: "📁 File Operations",
            CommandCategory.SYSTEM: "⚙️ System Management",
            CommandCategory.NETWORK: "🌐 Network Operations",
            CommandCategory.BUILD: "🔨 Build & Compile",
            CommandCategory.TEST: "🧪 Testing",
            CommandCategory.DEPLOY: "🚀 Deployment",
            CommandCategory.DATABASE: "🗄️ Database Operations",
            CommandCategory.EDIT: "✏️ File Editing",
            CommandCategory.OTHER: "📌 Other Commands",
        }
        return descriptions.get(category, "📌 Other Commands")


class TerminalRecorder:
    """Terminal session recorder"""

    def __init__(self, output_file: str):
        self.output_file = output_file
        self.session_data: List[CommandEntry] = []
        self.metadata: Optional[SessionMetadata] = None
        self.start_time: Optional[float] = None
        self.is_recording = False

    def start(self):
        """Start recording session"""
        self.start_time = time.time()
        self.is_recording = True

        # Get session metadata
        import getpass
        import socket
        self.metadata = SessionMetadata(
            session_id=f"session_{int(self.start_time)}",
            created_at=datetime.fromtimestamp(self.start_time).isoformat(),
            shell=os.environ.get('SHELL', '/bin/bash'),
            user=getpass.getuser(),
            hostname=socket.gethostname(),
            cwd=os.getcwd(),
            term_size=self._get_terminal_size(),
        )

        print(f"🎬 TermCast Recording Started")
        print(f"   Session ID: {self.metadata.session_id}")
        print(f"   Output: {self.output_file}")
        print(f"   Working Dir: {self.metadata.cwd}")
        print(f"   Type commands below. Enter 'exit' or press Ctrl+C to stop.\n")

    def _get_terminal_size(self) -> Tuple[int, int]:
        """Get current terminal size"""
        try:
            size = shutil.get_terminal_size()
            return (size.columns, size.lines)
        except:
            return (80, 24)

    def record_command(self, command: str, output: str, exit_code: int = 0, duration: float = 0.0):
        """Record a command execution"""
        if not self.is_recording:
            return

        category = CommandClassifier.classify(command)
        entry = CommandEntry(
            timestamp=time.time(),
            command=command,
            output=output,
            exit_code=exit_code,
            duration=duration,
            category=category.value,
        )
        self.session_data.append(entry)

    def stop(self):
        """Stop recording and save session"""
        if not self.is_recording:
            return

        self.is_recording = False
        end_time = time.time()

        if self.metadata:
            self.metadata.total_commands = len(self.session_data)
            self.metadata.duration_seconds = end_time - self.start_time

        self._save_session()

        print(f"\n✅ Recording Stopped")
        print(f"   Commands recorded: {len(self.session_data)}")
        print(f"   Duration: {self.metadata.duration_seconds:.1f}s")
        print(f"   Saved to: {self.output_file}")

    def _save_session(self):
        """Save session to file"""
        data = {
            'metadata': asdict(self.metadata) if self.metadata else {},
            'commands': [asdict(entry) for entry in self.session_data],
        }
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def interactive_record(self):
        """Start interactive recording session using script-like approach"""
        self.start()

        try:
            import subprocess
            import tempfile

            # Create a temporary script file for recording
            with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
                temp_log = f.name

            # Use script command if available
            script_path = shutil.which('script')

            if script_path:
                # Use system script command
                print(f"📝 Using system 'script' command for recording...\n")

                # Build the command
                cmd = [script_path, '-q', '-f', temp_log]

                # Run the recording session
                env = os.environ.copy()
                env['TERM'] = os.environ.get('TERM', 'xterm-256color')

                process = subprocess.Popen(
                    cmd,
                    stdin=sys.stdin,
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                    env=env
                )

                process.wait()

                # Parse the typescript log
                self._parse_typescript_log(temp_log)

            else:
                # Fallback: Simple command recording mode
                print(f"⚠️ 'script' command not found. Using simple recording mode.\n")
                self._simple_record_mode()

            # Cleanup
            if os.path.exists(temp_log):
                os.remove(temp_log)

        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"\n⚠️ Recording mode error: {e}")
            print("Switching to simple recording mode...")
            self._simple_record_mode()
        finally:
            self.stop()

    def _parse_typescript_log(self, log_file: str):
        """Parse typescript log file"""
        try:
            with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            # Simple parsing: look for command patterns
            lines = content.split('\n')
            current_command = None
            command_output = []
            command_start_time = time.time()

            for line in lines:
                # Look for shell prompt patterns
                if re.match(r'^\$\s+', line) or re.match(r'^[^\s]+@[^\s]+[:~]', line):
                    # Save previous command if exists
                    if current_command:
                        duration = time.time() - command_start_time
                        self.record_command(
                            current_command,
                            '\n'.join(command_output),
                            0,
                            duration
                        )
                        command_output = []

                    # Extract new command
                    match = re.search(r'\$\s+(.+)$', line)
                    if match:
                        current_command = match.group(1).strip()
                        command_start_time = time.time()
                    else:
                        current_command = None
                elif current_command:
                    command_output.append(line)

            # Save last command
            if current_command:
                duration = time.time() - command_start_time
                self.record_command(
                    current_command,
                    '\n'.join(command_output),
                    0,
                    duration
                )

        except Exception as e:
            print(f"Warning: Could not parse log: {e}")

    def _simple_record_mode(self):
        """Simple recording mode without script command"""
        print("Simple Recording Mode - Commands will be logged\n")

        while True:
            try:
                # Show prompt
                prompt = f"{self.metadata.user}@{self.metadata.hostname}:{self.metadata.cwd}$ "
                command = input(prompt)

                if command.strip().lower() in ['exit', 'quit']:
                    break

                if not command.strip():
                    continue

                # Execute command and capture output
                start_time = time.time()

                try:
                    result = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    output = result.stdout + result.stderr
                    exit_code = result.returncode
                except subprocess.TimeoutExpired:
                    output = "Command timed out after 5 minutes"
                    exit_code = -1
                except Exception as e:
                    output = str(e)
                    exit_code = -1

                duration = time.time() - start_time

                # Print output
                if output:
                    print(output, end='')
                    if not output.endswith('\n'):
                        print()

                # Record the command
                self.record_command(command, output, exit_code, duration)

            except KeyboardInterrupt:
                print("^C")
                continue
            except EOFError:
                break


class SessionPlayer:
    """Session replay controller"""

    def __init__(self, session_file: str):
        self.session_file = session_file
        self.data = None
        self.metadata = None
        self.commands: List[CommandEntry] = []

    def load(self):
        """Load session from file"""
        with open(self.session_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        meta = self.data['metadata']
        self.metadata = SessionMetadata(
            session_id=meta['session_id'],
            created_at=meta['created_at'],
            shell=meta['shell'],
            user=meta['user'],
            hostname=meta['hostname'],
            cwd=meta['cwd'],
            term_size=tuple(meta['term_size']),
            total_commands=meta.get('total_commands', 0),
            duration_seconds=meta.get('duration_seconds', 0.0),
        )
        self.commands = [CommandEntry(**cmd) for cmd in self.data['commands']]

    def play(self, speed: float = 1.0, interactive: bool = False):
        """Play back the session"""
        if not self.commands:
            print("❌ No commands to replay")
            return

        print(f"🎬 Playing Session: {self.metadata.session_id}")
        print(f"   Recorded: {self.metadata.created_at}")
        print(f"   Commands: {len(self.commands)}")
        print(f"   Speed: {speed}x\n")

        if interactive:
            self._interactive_play(speed)
        else:
            self._auto_play(speed)

    def _auto_play(self, speed: float):
        """Auto-play session"""
        for i, cmd in enumerate(self.commands, 1):
            print(f"\n{'─' * 60}")
            print(f"[{i}/{len(self.commands)}] $ {cmd.command}")
            print(f"{'─' * 60}")

            if cmd.output:
                print(cmd.output)

            if cmd.exit_code != 0:
                print(f"\n⚠️ Exit code: {cmd.exit_code}")

            # Simulate delay
            delay = min(cmd.duration / speed, 2.0)
            time.sleep(delay)

    def _interactive_play(self, speed: float):
        """Interactive playback with controls"""
        current_idx = 0

        while current_idx < len(self.commands):
            cmd = self.commands[current_idx]

            print(f"\n{'─' * 60}")
            print(f"[{current_idx + 1}/{len(self.commands)}] $ {cmd.command}")
            cat_enum = CommandCategory(cmd.category) if any(c.value == cmd.category for c in CommandCategory) else CommandCategory.OTHER
            print(f"Category: {CommandClassifier.get_description(cat_enum)}")
            print(f"{'─' * 60}")

            if cmd.output:
                print(cmd.output)

            if cmd.exit_code != 0:
                print(f"\n⚠️ Exit code: {cmd.exit_code}")

            print(f"\n[Enter: Next | b: Back | q: Quit | j: Jump | s: Stats]")
            choice = input("> ").strip().lower()

            if choice == 'q':
                break
            elif choice == 'b':
                current_idx = max(0, current_idx - 1)
            elif choice == 'j':
                try:
                    target = int(input(f"Jump to (1-{len(self.commands)}): ")) - 1
                    current_idx = max(0, min(target, len(self.commands) - 1))
                except ValueError:
                    current_idx += 1
            elif choice == 's':
                self._show_command_stats(cmd)
                continue
            else:
                current_idx += 1

    def _show_command_stats(self, cmd: CommandEntry):
        """Show detailed command statistics"""
        print(f"\n📊 Command Details:")
        print(f"   Command: {cmd.command}")
        print(f"   Category: {cmd.category}")
        print(f"   Duration: {cmd.duration:.2f}s")
        print(f"   Exit Code: {cmd.exit_code}")
        print(f"   Output Length: {len(cmd.output)} chars")
        print(f"   Timestamp: {datetime.fromtimestamp(cmd.timestamp)}")

    def export_text(self, output_file: str):
        """Export session as plain text"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# TermCast Session Export\n")
            f.write(f"# Session ID: {self.metadata.session_id}\n")
            f.write(f"# Recorded: {self.metadata.created_at}\n")
            f.write(f"# User: {self.metadata.user}@{self.metadata.hostname}\n")
            f.write(f"#\n\n")

            for i, cmd in enumerate(self.commands, 1):
                f.write(f"{'─' * 60}\n")
                f.write(f"[{i}] $ {cmd.command}\n")
                f.write(f"{'─' * 60}\n")
                if cmd.output:
                    f.write(cmd.output)
                    f.write("\n")
                f.write(f"# Duration: {cmd.duration:.2f}s | Exit: {cmd.exit_code}\n\n")

        print(f"✅ Exported to: {output_file}")

    def export_asciinema(self, output_file: str):
        """Export session in asciinema format"""
        # Asciinema v2 format
        header = {
            "version": 2,
            "width": self.metadata.term_size[0],
            "height": self.metadata.term_size[1],
            "timestamp": int(time.time()),
            "env": {"SHELL": self.metadata.shell, "TERM": "xterm-256color"}
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(header) + "\n")

            current_time = 0.0
            for cmd in self.commands:
                # Write command
                current_time += 0.1
                line = json.dumps([current_time, "o", f"$ {cmd.command}\r\n"])
                f.write(line + "\n")

                # Write output
                if cmd.output:
                    for out_line in cmd.output.split('\n'):
                        current_time += 0.01
                        line = json.dumps([current_time, "o", out_line + "\r\n"])
                        f.write(line + "\n")

                current_time += cmd.duration

        print(f"✅ Exported to: {output_file}")

    def show_stats(self):
        """Display session statistics"""
        print(f"\n📊 Session Statistics")
        print(f"{'─' * 50}")
        print(f"Session ID: {self.metadata.session_id}")
        print(f"Recorded: {self.metadata.created_at}")
        print(f"User: {self.metadata.user}@{self.metadata.hostname}")
        print(f"Shell: {self.metadata.shell}")
        print(f"Working Directory: {self.metadata.cwd}")
        print(f"Terminal Size: {self.metadata.term_size[0]}x{self.metadata.term_size[1]}")
        print(f"\nTotal Commands: {self.metadata.total_commands}")
        print(f"Total Duration: {self.metadata.duration_seconds:.1f}s")

        if not self.commands:
            return

        # Category breakdown
        categories = {}
        for cmd in self.commands:
            cat = cmd.category
            categories[cat] = categories.get(cat, 0) + 1

        print(f"\n📈 Command Categories:")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            pct = count / len(self.commands) * 100
            cat_enum = CommandCategory(cat) if any(c.value == cat for c in CommandCategory) else CommandCategory.OTHER
            desc = CommandClassifier.get_description(cat_enum)
            bar = '█' * int(pct / 5)
            print(f"   {desc}: {bar} {count} ({pct:.1f}%)")

        # Top commands
        print(f"\n🔝 Top Commands:")
        cmd_counts = {}
        for cmd in self.commands:
            base_cmd = cmd.command.split()[0] if cmd.command else ""
            if base_cmd:
                cmd_counts[base_cmd] = cmd_counts.get(base_cmd, 0) + 1

        for cmd, count in sorted(cmd_counts.items(), key=lambda x: -x[1])[:5]:
            bar = '●' * count
            print(f"   {cmd:12} {bar} {count}")

        # Success rate
        success_count = sum(1 for cmd in self.commands if cmd.exit_code == 0)
        success_rate = success_count / len(self.commands) * 100 if self.commands else 0
        print(f"\n✅ Success Rate: {success_rate:.1f}% ({success_count}/{len(self.commands)})")


class TermCastCLI:
    """Main CLI interface"""

    def __init__(self):
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser"""
        parser = argparse.ArgumentParser(
            prog='termcast',
            description='🎬 TermCast - Terminal Session Recording & Smart Replay Engine',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  termcast record                    # Start interactive recording
  termcast record -o session.json    # Record with custom output file
  termcast play session.json         # Play back a session
  termcast play session.json -i      # Interactive playback
  termcast stats session.json        # Show session statistics
  termcast export session.json -t text -o output.txt
  termcast list                      # List all recorded sessions

For more information: https://github.com/gitstq/termcast
            """
        )

        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Record command
        record_parser = subparsers.add_parser('record', help='Record a terminal session')
        record_parser.add_argument('-o', '--output', default='session.json',
                                   help='Output file (default: session.json)')

        # Play command
        play_parser = subparsers.add_parser('play', help='Play back a recorded session')
        play_parser.add_argument('file', help='Session file to play')
        play_parser.add_argument('-s', '--speed', type=float, default=1.0,
                                 help='Playback speed multiplier (default: 1.0)')
        play_parser.add_argument('-i', '--interactive', action='store_true',
                                 help='Interactive playback mode')

        # Stats command
        stats_parser = subparsers.add_parser('stats', help='Show session statistics')
        stats_parser.add_argument('file', help='Session file to analyze')

        # Export command
        export_parser = subparsers.add_parser('export', help='Export session to various formats')
        export_parser.add_argument('file', help='Session file to export')
        export_parser.add_argument('-t', '--type', choices=['text', 'asciinema', 'json'],
                                   default='text', help='Export format')
        export_parser.add_argument('-o', '--output', required=True,
                                   help='Output file')

        # List command
        list_parser = subparsers.add_parser('list', help='List recorded sessions')
        list_parser.add_argument('-d', '--directory', default='.',
                                 help='Directory to search for sessions')

        return parser

    def run(self, args: Optional[List[str]] = None):
        """Run the CLI"""
        parsed_args = self.parser.parse_args(args)

        if not parsed_args.command:
            self.parser.print_help()
            return

        try:
            if parsed_args.command == 'record':
                self._cmd_record(parsed_args)
            elif parsed_args.command == 'play':
                self._cmd_play(parsed_args)
            elif parsed_args.command == 'stats':
                self._cmd_stats(parsed_args)
            elif parsed_args.command == 'export':
                self._cmd_export(parsed_args)
            elif parsed_args.command == 'list':
                self._cmd_list(parsed_args)
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)

    def _cmd_record(self, args):
        """Handle record command"""
        recorder = TerminalRecorder(args.output)
        recorder.interactive_record()

    def _cmd_play(self, args):
        """Handle play command"""
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
            return

        player = SessionPlayer(args.file)
        player.load()
        player.play(speed=args.speed, interactive=args.interactive)

    def _cmd_stats(self, args):
        """Handle stats command"""
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
            return

        player = SessionPlayer(args.file)
        player.load()
        player.show_stats()

    def _cmd_export(self, args):
        """Handle export command"""
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
            return

        player = SessionPlayer(args.file)
        player.load()

        if args.type == 'text':
            player.export_text(args.output)
        elif args.type == 'asciinema':
            player.export_asciinema(args.output)
        elif args.type == 'json':
            shutil.copy(args.file, args.output)
            print(f"✅ Exported to: {args.output}")

    def _cmd_list(self, args):
        """Handle list command"""
        sessions = []
        for file in Path(args.directory).glob('*.json'):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    meta = data.get('metadata', {})
                    sessions.append({
                        'file': str(file),
                        'id': meta.get('session_id', 'unknown'),
                        'created': meta.get('created_at', 'unknown'),
                        'commands': len(data.get('commands', [])),
                        'duration': meta.get('duration_seconds', 0),
                    })
            except:
                pass

        if not sessions:
            print("📭 No recorded sessions found")
            return

        print(f"\n📼 Recorded Sessions ({len(sessions)} found):")
        print(f"{'─' * 80}")
        print(f"{'File':<25} {'Created':<20} {'Commands':<10} {'Duration':<10}")
        print(f"{'─' * 80}")

        for s in sorted(sessions, key=lambda x: x['created'], reverse=True):
            created = s['created'][:19] if len(s['created']) > 19 else s['created']
            print(f"{s['file']:<25} {created:<20} {s['commands']:<10} {s['duration']:.1f}s")


def main():
    """Entry point"""
    cli = TermCastCLI()
    cli.run()


if __name__ == '__main__':
    main()
