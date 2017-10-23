#!/usr/bin/env python
import json
import os
import sys

import toga

# For the moment, this is Cocoa specific.
from toga_cocoa.libs import NSObject, NSTimer, objc_method, SEL


CLEANSE = open(
    os.path.join(os.path.dirname(__file__), 'cleanse.js')
).read()


INSPECT = open(
    os.path.join(os.path.dirname(__file__), 'inspect.js')
).read()


TEST_CLASS_TEMPLATE = open(
    os.path.join(os.path.dirname(__file__), 'test_class.tpy')
).read()


class Loader(NSObject):
    @objc_method
    def run_(self, info) -> None:
        try:
            filename = os.path.abspath(next(self.filenames))

            self.webview.url = 'file://' + filename
            print("Inspecting {}...".format(filename))

            cleaner = Cleaner.alloc().init()
            cleaner.loader = self
            cleaner.webview = self.webview
            cleaner.filename = filename
            cleaner.output = self.output
            cleaner.path = self.path

            NSTimer.scheduledTimerWithTimeInterval(
                0.1,
                target=cleaner,
                selector=SEL('run:'),
                userInfo=None,
                repeats=False
            )
        except StopIteration:
            sys.exit(1)


class Cleaner(NSObject):
    @objc_method
    def run_(self, info) -> None:
        try:
            print("Cleaning {}...".format(self.filename))
            self.webview.evaluate(CLEANSE)

            evaluator = Evaluator.alloc().init()
            evaluator.loader = self.loader
            evaluator.webview = self.webview
            evaluator.filename = self.filename
            evaluator.output = self.output
            evaluator.path = self.path

            NSTimer.scheduledTimerWithTimeInterval(
                0.1,
                target=evaluator,
                selector=SEL('run:'),
                userInfo=None,
                repeats=False
            )
        except StopIteration:
            sys.exit(1)


class Evaluator(NSObject):
    @objc_method
    def run_(self, info) -> None:
        try:
            print("Inspecting {}...".format(self.filename))
            result = self.webview.evaluate(INSPECT)
            # print(result)
            result = json.loads(result)
            example = os.path.splitext(os.path.basename(self.filename))[0]

            test_dir = os.path.join(self.output, self.path.replace('-', '_'))

            # If a document has "matches" or "assert" metadata,
            # it's a test document; otherwise, it's a reference.
            # We can ignore reference files. They often don't have
            # the same document structure as the base document,
            # so they're not helpful for a DOM comparison.
            if 'matches' in result or 'assert' in result:
                newdirs = []
                dirname = test_dir
                while not os.path.exists(dirname):
                    newdirs.append(dirname)
                    dirname = os.path.dirname(dirname)

                newdirs.reverse()
                for newdir in newdirs:
                    print("Creating directory {}...".format(newdir))
                    os.mkdir(newdir)
                    with open(os.path.join(newdir, '__init__.py'), 'w'):
                        pass

                # Output the test case data

                # If the last part of the filename is of the pattern
                # -001 or -001a, then the group name drops that part.
                parts = example.rsplit('-')
                if parts[-1].isdigit() or parts[-1][:-1].isdigit():
                    parts.pop()
                    suffix = '-'
                else:
                    suffix = ''

                group = '-'.join(parts)
                group_class = 'Test' + ''.join(p.title() for p in parts)
                group_file = 'test_' + '_'.join(parts) + '.py'

                test_filename = os.path.join(test_dir, group_file)
                print("Writing unittest file {}".format(test_filename))
                with open(os.path.join(test_filename), 'w') as f:
                    f.write(TEST_CLASS_TEMPLATE.format(
                        group=group + suffix,
                        classname=group_class,
                    ))

                test_datadir = os.path.join(test_dir, 'data')
                # Create data/ref directory
                try:
                    os.mkdir(test_datadir)
                except FileExistsError:
                    pass

                test_datafile = os.path.join(test_datadir, example + '.json')

                # If this is a new test, automatically add it to the not_implemented file.
                if not os.path.exists(test_datafile):
                    print('New test - adding to not_implemented list...')
                    with open(os.path.join(test_dir, 'not_implemented'), 'a') as nif:
                        nif.write('{}\n'.format(example.replace('-', '_')))

                # Output JSON content
                with open(test_datafile, 'w') as f:
                    print("Writing data file {}".format(test_datafile))
                    f.write(json.dumps({
                            'test_case': result['test_case'],
                            'assert': result.get('assert', None),
                            'help': result['help'],
                            'matches': result.get('matches', None),
                        }, indent=4))

                # Output reference rendering data
                test_refdir = os.path.join(test_dir, 'ref')
                # Create data/ref directory
                try:
                    os.mkdir(test_refdir)
                except FileExistsError:
                    pass

                # Output JSON content
                test_reffile = os.path.join(test_refdir, example + '.json')
                with open(test_reffile, 'w') as f:
                    print("Writing reference file {}".format(test_reffile))
                    f.write(json.dumps(result['reference'], indent=4))

            NSTimer.scheduledTimerWithTimeInterval(
                0.05,
                target=self.loader,
                selector=SEL('run:'),
                userInfo=None,
                repeats=False
            )
        except StopIteration:
            sys.exit(1)


class W3CTestExtractor(toga.App):
    def startup(self):
        # We want the web canvas to be 1024x768;
        # 22 pixels is the window header size.
        self.main_window = toga.MainWindow(self.name, size=(1024, 768+22))
        self.main_window.app = self

        webview = toga.WebView()

        self.main_window.content = webview

        files = []
        filenames = [
            os.path.join(self.root, 'css', self.path, f)
            for f in os.listdir(os.path.join(self.root, 'css', self.path))
            if f.endswith('.xht') or f.endswith('.htm') or f.endswith('.html')
        ]

        loader = Loader.alloc().init()
        loader.webview = webview
        loader.filenames = iter(filenames)
        loader.path = self.path
        loader.output = self.output

        NSTimer.scheduledTimerWithTimeInterval(
            0.5,
            target=loader,
            selector=SEL('run:'),
            userInfo=None,
            repeats=False
        )

        # Show the main window
        self.main_window.show()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: w3c.py <base> <input> <output>")
        print()
        print("where: ")
        print("    <base>: root of the web-platform-tests checkout")
        print("    <input>: subdirectory of the web-platform-tests css test set to convert")
        print("    <output>: base output directory. Use 'debug' to dump the tests discovered")
        print()
        print("  e.g.: w3c.py ~/path/to/web-platform-tests CSS2/abspos ../tests")
        print()
        sys.exit(1)

    app = W3CTestExtractor('W3CTestExtractor', 'org.pybee.w3c')
    app.root = sys.argv[1]
    app.path = sys.argv[2]
    app.output = sys.argv[3]

    app.main_loop()
