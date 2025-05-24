"use client"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Sparkles, Save } from "lucide-react"

export function JournalContent() {
  const [content, setContent] = useState("")
  const [isPublic, setIsPublic] = useState(false)

  const todaysQuestion = "오늘 가장 감사했던 순간은 무엇인가요?"

  const handleSave = () => {
    console.log("저장됨:", content, "공개여부:", isPublic)
    // 여기에 저장 로직 추가
  }

  const handleAIAssist = () => {
    console.log("AI 도움 요청")
    // 여기에 AI 도움 로직 추가
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-xl">
          오늘 ({new Date().toLocaleDateString("ko-KR", { year: "numeric", month: "long", day: "numeric" })})의 질문
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="text-lg font-medium">{todaysQuestion}</div>

        <Textarea
          placeholder="여기에 답변을 작성하세요..."
          className="min-h-[200px] resize-none"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />

        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center space-x-4">
            <Button onClick={handleSave} className="flex items-center gap-2">
              <Save className="h-4 w-4" />
              저장하기
            </Button>
            <Button onClick={handleAIAssist} variant="outline" className="flex items-center gap-2">
              <Sparkles className="h-4 w-4" />
              AI 도움
            </Button>
          </div>

          <div className="flex items-center space-x-2">
            <Switch id="public-mode" checked={isPublic} onCheckedChange={setIsPublic} />
            <Label htmlFor="public-mode">{isPublic ? "공개" : "비공개"}</Label>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
