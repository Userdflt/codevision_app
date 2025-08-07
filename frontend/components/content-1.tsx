import Image from 'next/image'

export default function ContentSection() {
    return (
        <section className="py-16 md:py-32 bg-muted/30">
            <div className="mx-auto max-w-5xl space-y-8 px-6 md:space-y-16">
                <h2 className="relative z-10 max-w-xl text-4xl font-medium lg:text-5xl">Trusted by Building Professionals Across Australia</h2>
                <div className="grid gap-6 sm:grid-cols-2 md:gap-12 lg:gap-24">
                    <div className="relative mb-6 sm:mb-0">
                        <div className="aspect-square relative rounded-2xl bg-gradient-to-br from-primary/10 to-primary/20 p-8 flex items-center justify-center">
                            <div className="text-center space-y-4">
                                <div className="text-6xl font-bold text-primary">98%</div>
                                <div className="text-lg font-medium">Accuracy Rate</div>
                                <div className="text-sm text-muted-foreground">On building code interpretations</div>
                            </div>
                        </div>
                    </div>

                    <div className="relative space-y-4">
                        <p className="text-muted-foreground">
                            Code Vision has revolutionized how we approach building compliance. <span className="text-foreground font-bold">From architects to engineers</span>, professionals rely on our AI assistant for accurate, instant guidance.
                        </p>
                        <p className="text-muted-foreground">Whether you're working on residential projects or commercial developments, our comprehensive database ensures you have the right information at your fingertips.</p>

                        <div className="pt-6">
                            <blockquote className="border-l-4 border-primary pl-4">
                                <p className="text-foreground">"Code Vision has saved us countless hours of research. The AI provides accurate interpretations of complex building codes with reliable source references. It's become an essential tool for our design team."</p>

                                <div className="mt-6 space-y-3">
                                    <cite className="block font-medium text-foreground">Sarah Mitchell, Senior Architect</cite>
                                    <div className="text-sm text-muted-foreground">Mitchell & Associates Architecture</div>
                                </div>
                            </blockquote>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}
