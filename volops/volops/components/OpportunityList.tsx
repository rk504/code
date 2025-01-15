import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

export default function OpportunityList({ opportunities }) {
  return (
    <div className="p-6 space-y-6">
      {opportunities.map((opportunity) => (
        <Card key={opportunity.id} className="hover:shadow-lg transition-shadow duration-300">
          <CardContent className="p-6">
            <h3 className="text-lg font-semibold mb-2">{opportunity.title}</h3>
            <p className="text-sm text-gray-600 mb-2">{opportunity.organization}</p>
            <p className="text-sm mb-4">{opportunity.description}</p>
            <div className="flex items-center justify-between">
              <div className="flex space-x-2">
                <Badge variant="secondary">{opportunity.category}</Badge>
                <Badge variant="outline">{opportunity.commitment}</Badge>
              </div>
              <span className="text-sm text-gray-500">{opportunity.distance} km away</span>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

