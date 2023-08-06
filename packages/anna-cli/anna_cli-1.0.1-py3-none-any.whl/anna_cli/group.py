import click


class Anna(click.Group):
    def parse_args(self, ctx, args):
        if args[0] in self.commands:
            if len(args) == 1 or args[1] not in self.commands:
                args.insert(0, '')
        super(Anna, self).parse_args(ctx, args)
